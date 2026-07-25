from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError as DjangoValidationError

from config.logging import audit_log
from ..models import ClassBooking, ClassProgram, StudioClass
from users.exceptions import ServiceValidationError


class ClassService:
    """Encapsulates class and booking business logic."""

    @classmethod
    @transaction.atomic
    def create_class_booking(cls, program: ClassProgram, validated_data: dict) -> ClassBooking:
        try:
            booking = ClassBooking(**validated_data)
            booking.program = program
            booking.full_clean()
            booking.save()

            audit_log.info(
                action="class_booking.create",
                message=f"Booking created for program '{program.name}'",
                status="success",
                source="classes_app.services.class_services",
                extra={
                    "target_booking_id": str(booking.booking_id),
                    "target_program_id": str(program.program_id),
                },
            )
            return booking
        except DjangoValidationError as e:
            raise ServiceValidationError(
                e.message_dict if hasattr(e, "message_dict") else str(e)
            )
        except DatabaseError as e:
            audit_log.error(
                action="class_booking.create",
                message=f"Database error creating booking: {str(e)}",
                status="failed",
                source="classes_app.services.class_services",
                extra={"target_program_id": str(program.program_id) if program else None},
            )
            raise
