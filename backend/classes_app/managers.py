from django.db import models


class StudioClassManager(models.Manager):
    """Manager for StudioClass with active status helpers."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)


class ClassProgramManager(models.Manager):
    """Manager for ClassProgram with active status helpers."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)


class ClassBookingManager(models.Manager):
    """Manager for ClassBooking with read/unread helpers."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()

    def unread(self):
        return self.get_queryset().filter(is_read=False)

    def read(self):
        return self.get_queryset().filter(is_read=True)
