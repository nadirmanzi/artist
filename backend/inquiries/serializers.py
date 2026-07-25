from rest_framework import serializers

from catalog.models import Catalog
from catalog.serializers import EmbeddedCatalogSerializer
from inquiries.models import ArtworkInquiry, ContactInquiry


# -------------------------
# Contact Inquiry
# -------------------------


class ContactInquirySerializer(serializers.ModelSerializer):
    """Full read-only representation for list and retrieve endpoints."""

    class Meta:
        model = ContactInquiry
        fields = (
            "contact_inquiry_id",
            "name",
            "email",
            "phone_number",
            "message",
            "is_read",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CreateContactInquirySerializer(serializers.ModelSerializer):
    """Write serializer for public contact inquiry creation."""

    class Meta:
        model = ContactInquiry
        fields = (
            "name",
            "email",
            "phone_number",
            "message",
        )


class ContactInquiryStatusSerializer(serializers.ModelSerializer):
    """Lightweight serializer for staff mark_read responses."""

    class Meta:
        model = ContactInquiry
        fields = (
            "contact_inquiry_id",
            "is_read",
            "updated_at",
        )
        read_only_fields = fields


# -------------------------
# Artwork Inquiry
# -------------------------


class ArtworkInquirySerializer(serializers.ModelSerializer):
    """Full read-only representation for list and retrieve endpoints."""

    catalog = EmbeddedCatalogSerializer(read_only=True)

    class Meta:
        model = ArtworkInquiry
        fields = (
            "artwork_inquiry_id",
            "catalog",
            "name",
            "email",
            "phone_number",
            "message",
            "is_read",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CreateArtworkInquirySerializer(serializers.ModelSerializer):
    """Write serializer for public artwork inquiry creation."""

    catalog_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ArtworkInquiry
        fields = (
            "catalog_id",
            "name",
            "email",
            "phone_number",
            "message",
        )

    def validate_catalog_id(self, value):
        if not Catalog.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Catalog not found.")
        return value


class ArtworkInquiryStatusSerializer(serializers.ModelSerializer):
    """Lightweight serializer for staff mark_read responses."""

    class Meta:
        model = ArtworkInquiry
        fields = (
            "artwork_inquiry_id",
            "is_read",
            "updated_at",
        )
        read_only_fields = fields
