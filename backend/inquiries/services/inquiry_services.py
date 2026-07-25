from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError

from config.logging import audit_log
from users.exceptions import ServiceValidationError
from inquiries.models import ArtworkInquiry, ContactInquiry
from catalog.models import Catalog


class ContactInquiryService:
    """Encapsulates contact inquiry lifecycle operations."""

    @classmethod
    @transaction.atomic
    def create_contact_inquiry(cls, validated_data: dict) -> ContactInquiry:
        try:
            inquiry = ContactInquiry(**validated_data)
            inquiry.full_clean()
            inquiry.save()

            audit_log.info(
                action="contact_inquiry.create",
                message=f"Contact inquiry created from '{inquiry.email}'",
                status="success",
                source="inquiries.services.contact_inquiry_services",
                extra={"target_contact_inquiry_id": str(inquiry.contact_inquiry_id)},
            )
            return inquiry

        except DjangoValidationError as e:
            raise ServiceValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )
        except DatabaseError as e:
            audit_log.error(
                action="contact_inquiry.create",
                message=f"Database error creating contact inquiry: {str(e)}",
                status="failed",
                source="inquiries.services.contact_inquiry_services",
            )
            raise

    @classmethod
    @transaction.atomic
    def delete_contact_inquiry(cls, inquiry: ContactInquiry) -> None:
        inquiry_id = str(inquiry.contact_inquiry_id)
        try:
            inquiry.delete()
            audit_log.info(
                action="contact_inquiry.delete",
                message="Contact inquiry deleted permanently",
                status="success",
                source="inquiries.services.contact_inquiry_services",
                extra={"target_contact_inquiry_id": inquiry_id},
            )
        except DatabaseError as e:
            audit_log.error(
                action="contact_inquiry.delete",
                message=f"Database error deleting contact inquiry: {str(e)}",
                status="failed",
                source="inquiries.services.contact_inquiry_services",
                extra={"target_contact_inquiry_id": inquiry_id},
            )
            raise

    @classmethod
    @transaction.atomic
    def mark_as_read(cls, inquiry: ContactInquiry) -> ContactInquiry:
        try:
            inquiry.is_read = True
            inquiry.save(update_fields=["is_read", "updated_at"])
            audit_log.info(
                action="contact_inquiry.mark_read",
                message="Contact inquiry marked as read",
                status="success",
                source="inquiries.services.contact_inquiry_services",
                extra={"target_contact_inquiry_id": str(inquiry.contact_inquiry_id)},
            )
            return inquiry
        except DatabaseError as e:
            audit_log.error(
                action="contact_inquiry.mark_read",
                message=f"Database error marking contact inquiry as read: {str(e)}",
                status="failed",
                source="inquiries.services.contact_inquiry_services",
                extra={"target_contact_inquiry_id": str(inquiry.contact_inquiry_id)},
            )
            raise


class ArtworkInquiryService:
    """Encapsulates artwork inquiry lifecycle operations."""

    @classmethod
    @transaction.atomic
    def create_artwork_inquiry(
        cls, catalog: Catalog, validated_data: dict
    ) -> ArtworkInquiry:
        try:
            inquiry = ArtworkInquiry(**validated_data)
            inquiry.catalog = catalog
            inquiry.full_clean()
            inquiry.save()

            audit_log.info(
                action="artwork_inquiry.create",
                message=f"Artwork inquiry created for catalog '{catalog.name}'",
                status="success",
                source="inquiries.services.artwork_inquiry_services",
                extra={
                    "target_artwork_inquiry_id": str(inquiry.artwork_inquiry_id),
                    "target_catalog_id": str(catalog.catalog_id),
                },
            )
            return inquiry

        except DjangoValidationError as e:
            raise ServiceValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )
        except DatabaseError as e:
            audit_log.error(
                action="artwork_inquiry.create",
                message=f"Database error creating artwork inquiry: {str(e)}",
                status="failed",
                source="inquiries.services.artwork_inquiry_services",
                extra={"target_catalog_id": str(catalog.catalog_id)},
            )
            raise

    @classmethod
    @transaction.atomic
    def delete_artwork_inquiry(cls, inquiry: ArtworkInquiry) -> None:
        inquiry_id = str(inquiry.artwork_inquiry_id)
        try:
            inquiry.delete()
            audit_log.info(
                action="artwork_inquiry.delete",
                message="Artwork inquiry deleted permanently",
                status="success",
                source="inquiries.services.artwork_inquiry_services",
                extra={"target_artwork_inquiry_id": inquiry_id},
            )
        except DatabaseError as e:
            audit_log.error(
                action="artwork_inquiry.delete",
                message=f"Database error deleting artwork inquiry: {str(e)}",
                status="failed",
                source="inquiries.services.artwork_inquiry_services",
                extra={"target_artwork_inquiry_id": inquiry_id},
            )
            raise

    @classmethod
    @transaction.atomic
    def mark_as_read(cls, inquiry: ArtworkInquiry) -> ArtworkInquiry:
        try:
            inquiry.is_read = True
            inquiry.save(update_fields=["is_read", "updated_at"])
            audit_log.info(
                action="artwork_inquiry.mark_read",
                message="Artwork inquiry marked as read",
                status="success",
                source="inquiries.services.artwork_inquiry_services",
                extra={"target_artwork_inquiry_id": str(inquiry.artwork_inquiry_id)},
            )
            return inquiry
        except DatabaseError as e:
            audit_log.error(
                action="artwork_inquiry.mark_read",
                message=f"Database error marking artwork inquiry as read: {str(e)}",
                status="failed",
                source="inquiries.services.artwork_inquiry_services",
                extra={"target_artwork_inquiry_id": str(inquiry.artwork_inquiry_id)},
            )
            raise
