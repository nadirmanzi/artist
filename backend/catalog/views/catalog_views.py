"""
Catalog ViewSet: CRUD and visibility lifecycle actions for Catalog resources.

Handles:
- POST   /catalog/management/                   -> create (staff with add_catalog perm)
- GET    /catalog/management/                   -> list (staff with view_catalog perm)
- GET    /catalog/management/{pk}/              -> retrieve (staff with view_catalog perm)
- PUT    /catalog/management/{pk}/              -> update (staff with change_catalog perm)
- PATCH  /catalog/management/{pk}/             -> partial_update (staff with change_catalog perm)
- DELETE /catalog/management/{pk}/              -> destroy (superusers only)
- POST   /catalog/management/{pk}/publish/      -> publish (staff with can_publish_catalog perm)
- POST   /catalog/management/{pk}/archive/      -> archive (staff with can_archive_catalog perm)
- POST   /catalog/management/{pk}/set-draft/    -> set_draft (staff with change_catalog perm)

Permission model:
- Superusers: full access (CRUD + visibility actions + delete)
- Staff with view_catalog: list + retrieve
- Staff with add_catalog: create (catalog auto-tied to request.user)
- Staff with change_catalog: update/partial_update + set_draft
- Staff with can_publish_catalog: publish
- Staff with can_archive_catalog: archive
- Regular / unauthenticated users: no access

Design:
- Views only parse requests, check permissions, and return structured responses.
- All business logic and DB writes are delegated to CatalogService.
- Response structure mirrors users app (UserManagementViewSet) exactly:
    single resource  → {"catalog": {...}}
    list             → {"catalogs": [...]}
    action responses → {"<status_field>": ..., "catalog": {...}}
"""

import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from config.logging import audit_log
from catalog.models import Catalog
from catalog.serializers import (
    CatalogSerializer,
    CreateCatalogSerializer,
    UpdateCatalogSerializer,
    EmbeddedCatalogSerializer,
    StaffCatalogActionSerializer,
)
from catalog.utils.permissions import CatalogPermission
from catalog.services.catalog_services import CatalogService
from catalog.filters import CatalogFilter


logger = logging.getLogger(__name__)


@extend_schema_view(
    create=extend_schema(
        summary="Create Catalog",
        description="Create a new catalog entry. Auto-assigned to the requesting staff user.",
    ),
    list=extend_schema(
        summary="List Catalogs",
        description="List all catalogs. Staff with view_catalog permission only.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Catalog",
        description="Get a specific catalog's full details.",
    ),
    update=extend_schema(
        summary="Update Catalog",
        description="Full update of a catalog entry.",
    ),
    partial_update=extend_schema(
        summary="Partial Update Catalog",
        description="Partially update a catalog entry.",
    ),
    destroy=extend_schema(
        summary="Delete Catalog",
        description="Permanently delete a catalog (superusers only).",
    ),
)
class CatalogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Catalog CRUD and visibility lifecycle management.

    Responsibilities (view layer only):
    - Parse the incoming request
    - Check permissions (via get_permissions / CatalogPermission)
    - Delegate all state mutations to CatalogService
    - Return a consistent, uniform response structure

    All business logic and DB writes happen in CatalogService — NOT here.
    This mirrors the pattern established in UserManagementViewSet.
    """

    filter_backends = [DjangoFilterBackend]
    filterset_class = CatalogFilter

    def get_queryset(self):
        """
        Return queryset scoped to the requesting user's access level.

        - Superusers: all catalogs (select_related user for efficiency)
        - Staff with view_catalog: all catalogs (select_related user)
        - Others: empty queryset (permission layer should have blocked before here)

        Returns:
            QuerySet[Catalog]
        """
        user = self.request.user

        if user.is_superuser:
            return Catalog.objects.all()

        if user.is_staff and user.has_perm("catalog.view_catalog"):
            return Catalog.objects.all()


        # Safe fallback — permission layer should have blocked before reaching here
        return Catalog.objects.published()

    def get_serializer_class(self):
        """
        Return the appropriate serializer for the current action.

        Mapping:
        - create              → CreateCatalogSerializer  (write: validates fields only)
        - list                → CatalogSerializer        (read: full catalog + nested user)
        - retrieve            → CatalogSerializer        (read: full catalog + nested user)
        - update              → UpdateCatalogSerializer  (write: full update with uniqueness)
        - partial_update      → UpdateCatalogSerializer  (write: partial update with uniqueness)
        - publish/archive/set_draft → StaffCatalogActionSerializer (read: lightweight response)
        - destroy             → CatalogSerializer        (fallback, 204 returns no body)
        """
        if self.action == "create":
            return CreateCatalogSerializer
        if self.action in ["update", "partial_update"]:
            return UpdateCatalogSerializer
        if self.action in ["publish", "archive", "set_draft"]:
            return StaffCatalogActionSerializer
        return CatalogSerializer

    def get_permissions(self):
        """
        Return permission classes for the current action.

        All catalog actions require:
        - IsAuthenticated: user must be logged in
        - CatalogPermission: enforces fine-grained per-action rules

        Mirrors get_permissions() in UserManagementViewSet.
        """

        if self.action == "list":
            return [AllowAny()]

        return [IsAuthenticated(), CatalogPermission()]

    # -------------------------
    # LIST
    # -------------------------
    def list(self, request, *args, **kwargs):
        """
        List all catalogs accessible to the requesting user.

        GET /catalog/management/

        Returns:
            200: {"catalogs": [...]}  (paginated if pagination is configured)
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CatalogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CatalogSerializer(queryset, many=True)
        return Response({"catalogs": serializer.data})

    # -------------------------
    # RETRIEVE
    # -------------------------
    @extend_schema(
        summary="Full Catalog Detail",
        description="Return the full details of a specific catalog by pk (staff/admin only).",
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Return full catalog details.

        GET /catalog/management/{pk}/

        Returns:
            200: {"catalog": {...}}
            401: If user is not authenticated.
            403: If user is not staff/admin with view_catalog permission.
            404: If catalog does not exist.
        """
        catalog = self.get_object()
        serializer = CatalogSerializer(catalog)
        return Response({"catalog": serializer.data})

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, request, *args, **kwargs):
        """
        Create a new catalog, auto-assigning the owner to request.user.

        POST /catalog/management/
        Body: {
            "name": "...",
            "price": "...",
            "category": "...",
            "description": "...",
            "visibility_status": "..."
        }

        The 'user' field is never read from the request body.
        It is always set to request.user inside CatalogService.create_catalog().

        Returns:
            201: {"catalog": {...}}  (full CatalogSerializer including nested user)
            400: Validation errors.
            403: If user lacks add_catalog permission.
        """
        serializer = CreateCatalogSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Delegate the actual DB write to the service — view only validates
        catalog = CatalogService.create_catalog(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        audit_log.info(
            action="catalog.create",
            message=f"Catalog '{catalog.name}' created via API by user {request.user.user_id}",
            status="success",
            source="catalog.views.CatalogViewSet.create",
            extra={
                "target_catalog_id": str(catalog.catalog_id),
            }
        )

        return Response(
            {"catalog": CatalogSerializer(catalog).data},
            status=status.HTTP_201_CREATED,
        )

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, request, pk=None, *args, **kwargs):
        """
        Full or partial update of a catalog.

        PUT  /catalog/management/{pk}/   → full update (all fields required)
        PATCH /catalog/management/{pk}/  → partial update (subset of fields)

        Returns:
            200: {"catalog": {...}}
            400: Validation errors.
            403: If user lacks change_catalog permission.
            404: If catalog does not exist.
        """
        partial = kwargs.pop("partial", False)
        catalog = self.get_object()
        serializer = UpdateCatalogSerializer(
            catalog, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Delegate the DB write to the service — view only validates + delegates
        catalog = CatalogService.update_catalog(
            catalog=catalog,
            validated_data=serializer.validated_data,
        )

        return Response({"catalog": CatalogSerializer(catalog).data})

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partial update of a catalog (delegates to update with partial=True).

        PATCH /catalog/management/{pk}/

        Returns:
            200: {"catalog": {...}}
        """
        kwargs["partial"] = True
        return self.update(request, pk=pk, *args, **kwargs)

    # -------------------------
    # DESTROY
    # -------------------------
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Permanently delete a catalog (superusers only).

        DELETE /catalog/management/{pk}/

        Returns:
            204: No Content (empty body on success)
            403: If user is not a superuser.
            404: If catalog does not exist.
        """
        catalog = self.get_object()

        audit_log.warning(
            action="catalog.delete",
            message=(
                f"Catalog '{catalog.name}' deletion initiated "
                f"by superuser {request.user.user_id}"
            ),
            status="in_progress",
            source="catalog.views.CatalogViewSet.destroy",
            extra={
                "target_catalog_id": str(catalog.catalog_id),
            }
        )

        CatalogService.delete_catalog(catalog)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # -------------------------
    # CUSTOM VISIBILITY ACTIONS
    # -------------------------

    @extend_schema(
        summary="Publish Catalog",
        description="Transition catalog visibility to 'published' (requires can_publish_catalog perm).",
    )
    @action(detail=True, methods=["post"], url_path="publish")
    def publish(self, request, pk=None):
        """
        Publish a catalog (transition visibility_status to 'published').

        POST /catalog/management/{pk}/publish/

        Returns:
            200: {"visibility_status": "published", "catalog": {catalog_id, name, visibility_status, updated_at}}
            409: If catalog is already published.
            403: If user lacks can_publish_catalog permission.
        """
        catalog = self.get_object()
        catalog = CatalogService.publish_catalog(catalog)

        return Response(
            {
                "visibility_status": catalog.visibility_status,
                "catalog": StaffCatalogActionSerializer(catalog).data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Archive Catalog",
        description="Transition catalog visibility to 'archived' (requires can_archive_catalog perm).",
    )
    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, pk=None):
        """
        Archive a catalog (transition visibility_status to 'archived').

        POST /catalog/management/{pk}/archive/

        Returns:
            200: {"visibility_status": "archived", "catalog": {catalog_id, name, visibility_status, updated_at}}
            409: If catalog is already archived.
            403: If user lacks can_archive_catalog permission.
        """
        catalog = self.get_object()
        catalog = CatalogService.archive_catalog(catalog)

        return Response(
            {
                "visibility_status": catalog.visibility_status,
                "catalog": StaffCatalogActionSerializer(catalog).data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Set Draft",
        description="Revert catalog visibility back to 'draft' (requires change_catalog perm).",
    )
    @action(detail=True, methods=["post"], url_path="set-draft")
    def set_draft(self, request, pk=None):
        """
        Revert a catalog to draft status (transition visibility_status to 'draft').

        POST /catalog/management/{pk}/set-draft/

        Returns:
            200: {"visibility_status": "draft", "catalog": {catalog_id, name, visibility_status, updated_at}}
            409: If catalog is already in draft status.
            403: If user lacks change_catalog permission.
        """
        catalog = self.get_object()
        catalog = CatalogService.set_draft(catalog)

        return Response(
            {
                "visibility_status": catalog.visibility_status,
                "catalog": StaffCatalogActionSerializer(catalog).data,
            },
            status=status.HTTP_200_OK,
        )
