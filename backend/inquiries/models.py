import uuid

from django.db import models
from simple_history.models import HistoricalRecords

from catalog.models import Catalog
from inquiries.managers import ArtworkInquiryManager, ContactInquiryManager


class ContactInquiry(models.Model):
    contact_inquiry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = ContactInquiryManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contact inquiry from {self.name} ({self.email})"


class ArtworkInquiry(models.Model):
    artwork_inquiry_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    catalog = models.ForeignKey(
        Catalog, on_delete=models.CASCADE, related_name="artwork_inquiries"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = ArtworkInquiryManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Artwork inquiry for {self.catalog.name} by {self.email}"
