from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ClassBooking, ClassProgram, StudioClass


def _is_active_badge(is_active):
    if is_active:
        return mark_safe(
            '<span style="background-color: #2e7d32; color: white; padding: 3px 9px; '
            'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Active</span>'
        )
    return mark_safe(
        '<span style="background-color: #d32f2f; color: white; padding: 3px 9px; '
            'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Inactive</span>'
    )


def _is_read_badge(is_read):
    if is_read:
        return mark_safe(
            '<span style="background-color: #2e7d32; color: white; padding: 3px 9px; '
            'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Read</span>'
        )
    return mark_safe(
        '<span style="background-color: #f57c00; color: white; padding: 3px 9px; '
        'border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Unread</span>'
    )


@admin.register(StudioClass)
class StudioClassAdmin(admin.ModelAdmin):
    list_display = ("name", "active_badge", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active", "created_at")
    ordering = ["created_at"]
    
    readonly_fields = ["studio_class_id", "created_at", "updated_at"]
    
    fieldsets = (
        ("Core Information", {
            "fields": ("studio_class_id", "name", "description")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

    def active_badge(self, obj):
        return _is_active_badge(obj.is_active)
    active_badge.short_description = "Status"


@admin.register(ClassProgram)
class ClassProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "studio_class", "price", "sessions", "active_badge")
    list_filter = ("studio_class", "is_active")
    search_fields = ("name", "studio_class__name")
    list_select_related = ["studio_class"]
    ordering = ["created_at"]
    
    readonly_fields = ["program_id", "created_at", "updated_at"]

    fieldsets = (
        ("Program Identity", {
            "fields": ("program_id", "studio_class", "name")
        }),
        ("Details", {
            "fields": ("price", "sessions", "includes")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )

    def active_badge(self, obj):
        return _is_active_badge(obj.is_active)
    active_badge.short_description = "Status"


@admin.register(ClassBooking)
class ClassBookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "program", "name", "email", "phone_number", "read_badge", "created_at")
    list_filter = ("is_read", "program__studio_class", "created_at")
    search_fields = ("name", "email", "phone_number", "program__name")
    list_select_related = ["program"]
    ordering = ["-created_at"]
    
    readonly_fields = [
        "booking_id", "program", "name", "email", 
        "phone_number", "created_at", "updated_at"
    ]

    fieldsets = (
        ("Booking Information", {
            "fields": ("booking_id", "program")
        }),
        ("Client Details", {
            "fields": ("name", "email", "phone_number")
        }),
        ("Status", {
            "fields": ("is_read",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )
    
    actions = ["mark_as_read", "mark_as_unread"]

    def read_badge(self, obj):
        return _is_read_badge(obj.is_read)
    read_badge.short_description = "Status"

    @admin.action(description="Mark selected bookings as read")
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f"Successfully marked {count} bookings as read.")

    @admin.action(description="Mark selected bookings as unread")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f"Successfully marked {count} bookings as unread.")
