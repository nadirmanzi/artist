from django.db import models


class ContactInquiryManager(models.Manager):
    """Manager for ContactInquiry with read/unread status querysets."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()

    def unread(self):
        return self.get_queryset().filter(is_read=False)

    def read(self):
        return self.get_queryset().filter(is_read=True)


class ArtworkInquiryManager(models.Manager):
    """Manager for ArtworkInquiry with read/unread status querysets."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()

    def unread(self):
        return self.get_queryset().filter(is_read=False)

    def read(self):
        return self.get_queryset().filter(is_read=True)

    def for_catalog(self, catalog):
        return self.get_queryset().filter(catalog=catalog)


class InquiryManager(models.Manager):
    """Compatibility manager alias for legacy inquiry migrations."""

    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset()
