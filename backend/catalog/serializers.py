"""
Serializers for Catalog creation, retrieval, and updates.

This module provides DRF serializers for:
- EmbeddedCatalogSerializer: Minimal catalog representation for embedding in other resources
- CatalogSerializer: Full read-only representation for list/retrieve endpoints
- CreateCatalogSerializer: Write serializer for catalog creation (ties to request.user via service)
- UpdateCatalogSerializer: Write serializer for partial/full updates with uniqueness checks
- StaffCatalogActionSerializer: Lightweight representation for visibility action responses

Design mirrors the users app serializer pattern:
- Read serializers are strictly read_only
- Write serializers validate only the fields they accept
- All mutations go through CatalogUpdateMixin for atomic full_clean + save
- User assignment is always derived from request.user, never from request body
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from users.serializers import EmbeddedUserSerializer
from .models import Catalog


# -------------------------
# Shared mixin
# -------------------------
class CatalogUpdateMixin:
    """
    Mixin to provide a standardized atomic update with full_clean validation.

    Mirrors UserUpdateMixin from the users app — ensures model-level clean()
    is always called atomically before persisting. All UpdateCatalogSerializer
    instances inherit this so updates are never written without model validation.
    """

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            with transaction.atomic():
                instance.full_clean()
                instance.save()
        except DjangoValidationError as e:
            if hasattr(e, "message_dict"):
                raise serializers.ValidationError(e.message_dict)
            raise serializers.ValidationError(str(e))
        return instance


# -------------------------
# Embedded (for other resources)
# -------------------------
class EmbeddedCatalogSerializer(serializers.ModelSerializer):
    """
    Minimal catalog representation for embedding in other resource responses.

    Used inside action responses (publish, archive, set_draft) and anywhere
    a lightweight catalog reference is needed without the full payload.
    """

    class Meta:
        model = Catalog
        fields = ("catalog_id", "name", "price", "visibility_status")
        read_only_fields = fields


# -------------------------
# Full read representation (list + retrieve)
# -------------------------
class CatalogSerializer(serializers.ModelSerializer):
    """
    Full read-only catalog representation for list and retrieve endpoints.

    Includes a nested EmbeddedUserSerializer for the catalog owner so consumers
    receive the complete catalog context without making additional requests.
    All fields are read-only — this serializer is never used for writes.
    """

    user = EmbeddedUserSerializer(read_only=True)

    class Meta:
        model = Catalog
        fields = (
            "catalog_id",
            "name",
            "description",
            "price",
            "category",
            "dimensions",
            "image",
            "user",
            "visibility_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


# -------------------------
# Create serializer (POST)
# -------------------------
class CreateCatalogSerializer(serializers.ModelSerializer):
    """
    Serializer for new catalog creation.

    Validates all writable fields at the serializer level.  The actual catalog
    instance is created by CatalogService.create_catalog() — this serializer
    only validates and surfaces validated_data; it does NOT call .save() or
    assign the user (both are the service's responsibility).

    Validation:
    - price: must be >= 0
    - name: required, stripped, globally unique (case-insensitive)
    - visibility_status: must be a valid VisibilityStatus choice (default: draft)
    """

    class Meta:
        model = Catalog
        fields = (
            "name",
            "description",
            "price",
            "category",
            "dimensions",
            "image",
            "visibility_status",
        )

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        value = value.strip()
        if Catalog.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A catalog with this name already exists."
            )
        return value


# -------------------------
# Update serializer (PUT / PATCH)
# -------------------------
class UpdateCatalogSerializer(CatalogUpdateMixin, serializers.ModelSerializer):
    """
    Serializer for updating an existing catalog (PUT / PATCH).

    All fields are optional to support partial updates.
    Uniqueness check for name excludes the current instance.
    Uses CatalogUpdateMixin for an atomic full_clean() + save() cycle —
    model-level constraints are always enforced on write.

    Validation:
    - price: must be >= 0 if provided
    - name: stripped, unique excluding self if provided
    """

    class Meta:
        model = Catalog
        fields = (
            "name",
            "description",
            "price",
            "category",
            "dimensions",
            "image",
            "visibility_status",
        )

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        value = value.strip()
        if (
            Catalog.objects.filter(name__iexact=value)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                "A catalog with this name already exists."
            )
        return value


# -------------------------
# Staff / action serializer (visibility transitions)
# -------------------------
class StaffCatalogActionSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for staff-triggered visibility action responses.

    Mirrors StaffUserActionSerializer from the users app.
    Used as the response body for publish, archive, and set_draft actions
    where only state-relevant fields need to be returned.
    All fields are read-only — this serializer is never used for writes.
    """

    class Meta:
        model = Catalog
        fields = (
            "catalog_id",
            "name",
            "visibility_status",
            "updated_at",
        )
        read_only_fields = fields
