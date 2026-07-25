import uuid

from django.db import models
from simple_history.models import HistoricalRecords

from classes_app.managers import ClassBookingManager, ClassProgramManager, StudioClassManager


class StudioClass(models.Model):
    """A class category (e.g. Beginner Classes, Advanced Classes)."""

    studio_class_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = StudioClassManager()

    class Meta:
        db_table = "studio_class"
        ordering = ["created_at"]
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name


class ClassProgram(models.Model):
    """A program/package offered within a class category."""

    program_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studio_class = models.ForeignKey(
        StudioClass, on_delete=models.CASCADE, related_name="programs"
    )
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    sessions = models.PositiveIntegerField()
    includes = models.JSONField(default=list)
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = ClassProgramManager()

    class Meta:
        db_table = "class_program"
        ordering = ["created_at"]
        unique_together = [["studio_class", "name"]]

    def __str__(self):
        return f"{self.studio_class.name} — {self.name}"


class ClassBooking(models.Model):
    """A booking request for a specific class program."""

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(
        ClassProgram, on_delete=models.CASCADE, related_name="bookings"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = ClassBookingManager()

    class Meta:
        db_table = "class_booking"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking for {self.program.name} by {self.email}"
