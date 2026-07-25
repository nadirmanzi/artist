from django.contrib import admin

from .models import ClassBooking, ClassProgram, StudioClass


@admin.register(StudioClass)
class StudioClassAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(ClassProgram)
class ClassProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "studio_class", "price", "sessions", "is_active")
    list_filter = ("studio_class", "is_active")
    search_fields = ("name",)


@admin.register(ClassBooking)
class ClassBookingAdmin(admin.ModelAdmin):
    list_display = ("program", "name", "email", "phone_number", "is_read", "created_at")
    list_filter = ("is_read", "program__studio_class")
    search_fields = ("name", "email", "phone_number")
