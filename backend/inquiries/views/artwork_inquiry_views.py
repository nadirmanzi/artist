import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view

from catalog.models import Catalog
from inquiries.models import ArtworkInquiry
from inquiries.serializers import (
    ArtworkInquirySerializer,
    CreateArtworkInquirySerializer,
    ArtworkInquiryStatusSerializer,
)
from inquiries.utils.permissions import ArtworkInquiryPermission
from inquiries.services.inquiry_services import ArtworkInquiryService
from inquiries.views.contact_inquiry_views import InquiryThrottle


logger = logging.getLogger(__name__)


@extend_schema_view(
    create=extend_schema(
        summary="Create Artwork Inquiry",
        description="Submit a new artwork inquiry (public).",
    ),
    list=extend_schema(
        summary="List Artwork Inquiries",
        description="List all artwork inquiries (staff only).",
    ),
    retrieve=extend_schema(
        summary="Retrieve Artwork Inquiry",
        description="Get a specific artwork inquiry's details.",
    ),
    destroy=extend_schema(
        summary="Delete Artwork Inquiry",
        description="Permanently delete an artwork inquiry (superusers only).",
    ),
)
class ArtworkInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for ArtworkInquiry CRUD."""

    http_method_names = ["get", "post", "delete", "head", "options"]
    throttle_classes = [InquiryThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (
            user.is_staff and user.has_perm("inquiries.view_artworkinquiry")
        ):
            return ArtworkInquiry.objects.select_related("catalog").all()
        return ArtworkInquiry.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateArtworkInquirySerializer
        if self.action == "mark_read":
            return ArtworkInquiryStatusSerializer
        return ArtworkInquirySerializer

    def get_permissions(self):
        return [ArtworkInquiryPermission()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArtworkInquirySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ArtworkInquirySerializer(queryset, many=True)
        return Response({"artwork_inquiries": serializer.data})

    def retrieve(self, request, pk=None, *args, **kwargs):
        inquiry = self.get_object()
        serializer = ArtworkInquirySerializer(inquiry)
        return Response({"artwork_inquiry": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = CreateArtworkInquirySerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        catalog_id = serializer.validated_data.pop("catalog_id")
        catalog = Catalog.objects.get(pk=catalog_id)

        inquiry = ArtworkInquiryService.create_artwork_inquiry(
            catalog=catalog, validated_data=serializer.validated_data
        )

        return Response(
            {"artwork_inquiry": ArtworkInquirySerializer(inquiry).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        inquiry = self.get_object()
        ArtworkInquiryService.delete_artwork_inquiry(inquiry)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Mark Artwork Inquiry as Read",
        description="Mark an artwork inquiry as read (requires change_artworkinquiry perm).",
    )
    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        inquiry = self.get_object()
        inquiry = ArtworkInquiryService.mark_as_read(inquiry)

        return Response(
            {
                "is_read": inquiry.is_read,
                "artwork_inquiry": ArtworkInquiryStatusSerializer(inquiry).data,
            },
            status=status.HTTP_200_OK,
        )
