"""
Catalog management service: atomic lifecycle operations for Catalog records.

Encapsulates all business logic for catalog CRUD and visibility state transitions
so views don't need to know field names or validation rules. Views are responsible
only for parsing requests and checking permissions; all DB writes happen here.

Methods raise typed exceptions from users.exceptions on failure, which are
handled by the global DRF exception handler in config/exceptions.py.

Methods:
- create_catalog: Atomically create and persist a new catalog tied to request.user
- update_catalog: Atomically update catalog fields with full model validation
- delete_catalog: Permanently delete a catalog (superuser-only guard at view level)
- publish_catalog: Transition visibility to 'published'
- archive_catalog: Transition visibility to 'archived'
- set_draft: Revert visibility to 'draft'

All methods are @transaction.atomic — partial writes never reach the database.
All methods return the updated Catalog instance on success.
"""

from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError

from config.logging import audit_log
from users.exceptions import (
    ConflictError,
    ServiceValidationError,
)

from catalog.models import Catalog


class CatalogService:
    """
    Encapsulates catalog lifecycle operations.

    All mutating methods are atomic transactions. On success they return the
    updated Catalog instance. On failure they raise a specific ServiceError
    subclass (ConflictError, ServiceValidationError) which the global exception
    handler maps to the appropriate HTTP status code.

    Views must NOT perform DB writes directly — they delegate entirely to this
    service, mirroring the pattern established in UserManagementService.
    """

    @classmethod
    @transaction.atomic
    def create_catalog(cls, user, validated_data: dict) -> Catalog:
        """
        Atomically create a new catalog tied to the given user (request.user).

        The user field is ALWAYS derived from the calling view's request.user —
        it is never sourced from request.data. This ensures catalog ownership
        integrity regardless of what the client sends.

        Args:
            user: The User instance (request.user) to assign as catalog owner.
            validated_data: Dict of validated fields from CreateCatalogSerializer.

        Returns:
            Catalog: The newly created and persisted catalog instance.

        Raises:
            ServiceValidationError: If model-level validation (full_clean) fails.
            DatabaseError: On DB-level failures (propagated after audit log).

        Audit:
            Logs 'catalog.create' at INFO on success, ERROR on failure.
        """
        try:
            catalog = Catalog(**validated_data)
            catalog.user = user  # Always tied to request.user, never from body
            catalog.full_clean()
            catalog.save()

            audit_log.info(
                action="catalog.create",
                message=f"Catalog '{catalog.name}' created by user {user.user_id}",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            return catalog

        except DjangoValidationError as e:
            raise ServiceValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )
        except DatabaseError as e:
            audit_log.error(
                action="catalog.create",
                message=f"Database error creating catalog: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
            )
            raise

    @classmethod
    @transaction.atomic
    def update_catalog(cls, catalog: Catalog, validated_data: dict) -> Catalog:
        """
        Atomically update catalog fields with model-level validation.

        Applies all fields from validated_data onto the catalog instance, then
        runs full_clean() before saving to enforce all model-level constraints.
        The user/owner field is never modified here.

        Args:
            catalog: The Catalog instance to update.
            validated_data: Dict of fields to update (from UpdateCatalogSerializer).

        Returns:
            Catalog: The updated catalog instance.

        Raises:
            ServiceValidationError: If model-level validation fails.
            DatabaseError: On DB-level failures (propagated after audit log).

        Audit:
            Logs 'catalog.update' at INFO on success, ERROR on failure.
            Includes which fields were updated in the extra payload.
        """
        for attr, value in validated_data.items():
            setattr(catalog, attr, value)

        try:
            catalog.full_clean()
            catalog.save()

            audit_log.info(
                action="catalog.update",
                message=f"Catalog '{catalog.name}' updated",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
                extra={"updated_fields": list(validated_data.keys())},
            )
            return catalog

        except DjangoValidationError as e:
            raise ServiceValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )
        except DatabaseError as e:
            audit_log.error(
                action="catalog.update",
                message=f"Database error updating catalog: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            raise

    @classmethod
    @transaction.atomic
    def delete_catalog(cls, catalog: Catalog) -> None:
        """
        Permanently delete a catalog record (hard delete — irreversible).

        The view layer is responsible for ensuring only superusers can reach this
        method. This service does not perform permission checks — it assumes the
        caller has already verified authorization.

        Args:
            catalog: The Catalog instance to delete.

        Raises:
            DatabaseError: On DB-level failure (propagated after audit log).

        Audit:
            Logs 'catalog.delete' at INFO on success, ERROR on failure.
            The catalog_id and name are captured before deletion for the log.
        """
        catalog_id = str(catalog.catalog_id)
        catalog_name = catalog.name

        try:
            catalog.delete()

            audit_log.info(
                action="catalog.delete",
                message=f"Catalog '{catalog_name}' permanently deleted",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=catalog_id,
            )

        except DatabaseError as e:
            audit_log.error(
                action="catalog.delete",
                message=f"Database error deleting catalog: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
                target_catalog_id=catalog_id,
            )
            raise

    @classmethod
    @transaction.atomic
    def publish_catalog(cls, catalog: Catalog) -> Catalog:
        """
        Transition catalog visibility to 'published'.

        Args:
            catalog: Catalog instance to publish.

        Returns:
            Catalog: Updated catalog instance with visibility_status='published'.

        Raises:
            ConflictError: If catalog is already published.
            DatabaseError: On DB-level failure (propagated after audit log).

        Audit:
            Logs 'catalog.publish' at INFO on success, ERROR on failure.
        """
        if catalog.visibility_status == Catalog.VisibilityStatus.PUBLISHED:
            raise ConflictError("Catalog is already published.")

        try:
            catalog.visibility_status = Catalog.VisibilityStatus.PUBLISHED
            catalog.save(update_fields=["visibility_status", "updated_at"])

            audit_log.info(
                action="catalog.publish",
                message=f"Catalog '{catalog.name}' published",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            return catalog

        except DatabaseError as e:
            audit_log.error(
                action="catalog.publish",
                message=f"Database error publishing catalog: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            raise

    @classmethod
    @transaction.atomic
    def archive_catalog(cls, catalog: Catalog) -> Catalog:
        """
        Transition catalog visibility to 'archived'.

        Args:
            catalog: Catalog instance to archive.

        Returns:
            Catalog: Updated catalog instance with visibility_status='archived'.

        Raises:
            ConflictError: If catalog is already archived.
            DatabaseError: On DB-level failure (propagated after audit log).

        Audit:
            Logs 'catalog.archive' at WARNING on success (archiving is notable),
            ERROR on failure.
        """
        if catalog.visibility_status == Catalog.VisibilityStatus.ARCHIVED:
            raise ConflictError("Catalog is already archived.")

        try:
            catalog.visibility_status = Catalog.VisibilityStatus.ARCHIVED
            catalog.save(update_fields=["visibility_status", "updated_at"])

            audit_log.warning(
                action="catalog.archive",
                message=f"Catalog '{catalog.name}' archived",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            return catalog

        except DatabaseError as e:
            audit_log.error(
                action="catalog.archive",
                message=f"Database error archiving catalog: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            raise

    @classmethod
    @transaction.atomic
    def set_draft(cls, catalog: Catalog) -> Catalog:
        """
        Revert catalog visibility back to 'draft'.

        Args:
            catalog: Catalog instance to revert to draft status.

        Returns:
            Catalog: Updated catalog instance with visibility_status='draft'.

        Raises:
            ConflictError: If catalog is already in draft status.
            DatabaseError: On DB-level failure (propagated after audit log).

        Audit:
            Logs 'catalog.set_draft' at INFO on success, ERROR on failure.
        """
        if catalog.visibility_status == Catalog.VisibilityStatus.DRAFT:
            raise ConflictError("Catalog is already in draft status.")

        try:
            catalog.visibility_status = Catalog.VisibilityStatus.DRAFT
            catalog.save(update_fields=["visibility_status", "updated_at"])

            audit_log.info(
                action="catalog.set_draft",
                message=f"Catalog '{catalog.name}' reverted to draft",
                status="success",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            return catalog

        except DatabaseError as e:
            audit_log.error(
                action="catalog.set_draft",
                message=f"Database error setting catalog to draft: {str(e)}",
                status="failed",
                source="catalog.services.catalog_services",
                target_catalog_id=str(catalog.catalog_id),
            )
            raise
