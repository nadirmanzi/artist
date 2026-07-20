from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum, F
from django.utils import timezone
from .models import Catalog
from config.logging import audit_log  # Reusing your logging pattern

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    # Performance optimization: preload the owner user mapping
    list_select_related = ["user"]
    ordering = ["-created_at"]

    list_display = [
        "thumbnail_preview",
        "name",
        "category_badge",
        "formatted_price",
        "visibility_badge",
        "user",
        "created_at",
    ]

    search_fields = ["name", "description", "catalog_id", "user__email", "user__full_name"]

    readonly_fields = [
        "catalog_id",
        "thumbnail_large",
        "created_at",
        "updated_at",
    ]

    actions = [
        "bulk_publish",
        "bulk_archive",
        "calculate_total_value"
    ]

    def get_queryset(self, request):
        """Limit view to non-superusers if necessary, or preserve scope."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Staff users can only manage catalogs they own
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Automatically tag the creator if saving from the admin pane."""
        if not change or not obj.user_id:
            obj.user = request.user
        
        # Explicit model validation invocation before DB commit
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        """Structured visual columns for form organization."""
        if not obj:
            # Creation Layout
            return (
                (
                    "Identity & Classification",
                    {
                        "fields": ("name", "category", "description")
                    },
                ),
                (
                    "Financials & Physical Specs",
                    {
                        "fields": ("price", "dimensions")
                    },
                ),
                (
                    "Media Assets",
                    {
                        "fields": ("image",),
                        "description": "Upload high-quality portfolio images here."
                    },
                ),
                (
                    "Workflow",
                    {
                        "fields": ("visibility_status",)
                    },
                ),
            )
        else:
            # Modification Layout
            return (
                (
                    "Core Details",
                    {
                        "fields": (
                            "catalog_id",
                            "name",
                            "category",
                            "description",
                        )
                    },
                ),
                (
                    "Commercial Elements",
                    {
                        "fields": ("price", "dimensions"),
                    },
                ),
                (
                    "Visual Asset",
                    {
                        "fields": ("image", "thumbnail_large"),
                    },
                ),
                (
                    "Management Context",
                    {
                        "fields": ("user", "visibility_status"),
                    },
                ),
                (
                    "System Properties",
                    {
                        "classes": ("collapse",),
                        "fields": ("created_at", "updated_at"),
                    },
                ),
            )

    # --- HTML Formatting Badges ---

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return mark_safe('<span style="color: #bdc3c7; font-size: 11px;">No Image</span>')

    def thumbnail_large(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></a><br/><small style="color: #7f8c8d;">Click image to open original</small>',
                obj.image.url
            )
        return "No image uploaded yet."

    def formatted_price(self, obj):
        return f"${obj.price:,.2f}"

    def category_badge(self, obj):
        colors = {
            "landscapes": "#27ae60",
            "portraits": "#2980b9",
            "mixed_media": "#8e44ad",
            "other": "#7f8c8d"
        }
        color = colors.get(obj.category, "#7f8c8d")
        return format_html(
            '<span style="color: {}; font-weight: 600; text-transform: capitalize;">{}</span>',
            color, obj.get_category_display()
        )

    def visibility_badge(self, obj):
        if obj.visibility_status == Catalog.VisibilityStatus.PUBLISHED:
            return mark_safe(
                '<span style="background-color: #2e7d32; color: white; padding: 3px 9px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Published</span>'
            )
        elif obj.visibility_status == Catalog.VisibilityStatus.DRAFT:
            return mark_safe(
                '<span style="background-color: #f57c00; color: white; padding: 3px 9px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Draft</span>'
            )
        return mark_safe(
            '<span style="background-color: #37474f; color: white; padding: 3px 9px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;">Archived</span>'
        )

    thumbnail_preview.short_description = "Preview"
    thumbnail_large.short_description = "Current Asset"
    formatted_price.short_description = "Price"
    category_badge.short_description = "Category"
    visibility_badge.short_description = "Status"

    # --- Actions Architecture ---

    @admin.action(description="Publish selected portfolio assets")
    def bulk_publish(self, request, queryset):
        with transaction.atomic():
            count = queryset.update(visibility_status=Catalog.VisibilityStatus.PUBLISHED)
            for item in queryset:
                audit_log.info(
                    action="admin.catalog_publish",
                    message=f"Catalog asset '{item.name}' published manually via Django admin panel.",
                    status="success",
                    source="catalog.admin.CatalogAdmin",
                    target_catalog_id=str(item.catalog_id),
                )
        self.message_user(request, f"Successfully published {count} items.")

    @admin.action(description="Archive selected portfolio assets")
    def bulk_archive(self, request, queryset):
        with transaction.atomic():
            count = queryset.update(visibility_status=Catalog.VisibilityStatus.ARCHIVED)
            for item in queryset:
                audit_log.warning(
                    action="admin.catalog_archive",
                    message=f"Catalog asset '{item.name}' archived manually via Django admin panel.",
                    status="success",
                    source="catalog.admin.CatalogAdmin",
                    target_catalog_id=str(item.catalog_id),
                )
        self.message_user(request, f"Successfully archived {count} items.")

    @admin.action(description="Calculate total value of selected items")
    def calculate_total_value(self, request, queryset):
        summary = queryset.aggregate(total=Sum('price'))
        total_value = summary['total'] or 0
        self.message_user(
            request, 
            f"The combined valuation of the {queryset.count()} selected items is: ${total_value:,.2f}"
        )