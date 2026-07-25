from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from simple_history.models import HistoricalRecords

from .managers import CatalogManager


class Catalog(models.Model):
    class VisibilityStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    class CategoryChoices(models.TextChoices):
        LANDSCAPES = "landscapes", "Landscapes"
        PORTRAITS = "portraits", "Portraits"
        MIXED_MEDIA = "mixed_media", "Mixed Media"
        OTHER = "other", "Other"


    catalog_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(unique=True, max_length=255)

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    category = models.CharField(
        max_length=20, choices=CategoryChoices.choices, null=True, blank=True
    )

    dimensions = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to='catalog/images/', blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="catalogs"
    )

    visibility_status = models.CharField(
        max_length=20,
        choices=VisibilityStatus.choices,
        default=VisibilityStatus.DRAFT,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = CatalogManager()

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_publish_catalog", "Can publish a catalog"),
            ("can_archive_catalog", "Can archive a catalog"),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValidationError({"price": "Price cannot be negative."})


