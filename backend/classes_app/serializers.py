from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import ClassBooking, ClassProgram, StudioClass


class EmbeddedClassProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassProgram
        fields = ("program_id", "name", "price", "sessions", "includes")
        read_only_fields = fields


class ClassProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassProgram
        fields = (
            "program_id",
            "name",
            "price",
            "sessions",
            "includes",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class StudioClassSerializer(serializers.ModelSerializer):
    programs = ClassProgramSerializer(many=True, read_only=True)

    class Meta:
        model = StudioClass
        fields = (
            "studio_class_id",
            "name",
            "description",
            "is_active",
            "programs",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CreateClassBookingSerializer(serializers.ModelSerializer):
    program_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = ClassBooking
        fields = ("program_id", "name", "email", "phone_number")

    def validate_program_id(self, value):
        if not ClassProgram.objects.filter(pk=value, is_active=True).exists():
            raise serializers.ValidationError("Program not found or inactive.")
        return value


class ClassBookingSerializer(serializers.ModelSerializer):
    program = EmbeddedClassProgramSerializer(read_only=True)

    class Meta:
        model = ClassBooking
        fields = (
            "booking_id",
            "program",
            "name",
            "email",
            "phone_number",
            "is_read",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class ClassBookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBooking
        fields = ("booking_id", "is_read", "updated_at")
        read_only_fields = fields
