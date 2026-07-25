from django.contrib import admin
from django.utils.safestring import mark_safe

from inquiries.forms import ArtworkInquiryAdminForm, ContactInquiryAdminForm
from inquiries.models import ArtworkInquiry, ContactInquiry


def _is_read_badge(obj):
    if obj.is_read:
        return mark_safe(
            '<span style="background-color: #2e7d32; color: white; padding: 3px 9px; '
            'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Read</span>'
        )
    return mark_safe(
        '<span style="background-color: #d32f2f; color: white; padding: 3px 9px; '
        'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Unread</span>'
    )


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    form = ContactInquiryAdminForm
    ordering = ["-created_at"]

    list_display = [
        "contact_inquiry_id",
        "name",
        "email",
        "is_read_badge",
        "created_at",
    ]

    search_fields = ["name", "email", "message"]
    list_filter = ["is_read", "created_at"]

    readonly_fields = [
        "contact_inquiry_id",
        "name",
        "email",
        "phone_number",
        "message",
        "created_at",
        "updated_at",
    ]

    actions = ["mark_as_read", "mark_as_unread"]

    def is_read_badge(self, obj):
        return _is_read_badge(obj)

    is_read_badge.short_description = "Status"

    @admin.action(description="Mark selected contact inquiries as read")
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(
            request, f"Successfully marked {count} contact inquiries as read."
        )

    @admin.action(description="Mark selected contact inquiries as unread")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(
            request, f"Successfully marked {count} contact inquiries as unread."
        )


@admin.register(ArtworkInquiry)
class ArtworkInquiryAdmin(admin.ModelAdmin):
    form = ArtworkInquiryAdminForm
    list_select_related = ["catalog"]
    ordering = ["-created_at"]

    list_display = [
        "artwork_inquiry_id",
        "catalog",
        "name",
        "email",
        "is_read_badge",
        "created_at",
    ]

    search_fields = ["name", "email", "message", "catalog__name"]
    list_filter = ["is_read", "created_at"]

    readonly_fields = [
        "artwork_inquiry_id",
        "catalog",
        "name",
        "email",
        "phone_number",
        "message",
        "created_at",
        "updated_at",
    ]

    actions = ["mark_as_read", "mark_as_unread"]

    def is_read_badge(self, obj):
        return _is_read_badge(obj)

    is_read_badge.short_description = "Status"

    @admin.action(description="Mark selected artwork inquiries as read")
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(
            request, f"Successfully marked {count} artwork inquiries as read."
        )

    @admin.action(description="Mark selected artwork inquiries as unread")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(
            request, f"Successfully marked {count} artwork inquiries as unread."
        )
