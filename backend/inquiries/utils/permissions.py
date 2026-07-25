from rest_framework import permissions


class ContactInquiryPermission(permissions.BasePermission):
    """Permission class for contact inquiry management."""

    def has_permission(self, request, view):
        user = request.user

        if view.action == "create":
            return True

        if user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return user.is_staff and user.has_perm("inquiries.view_contactinquiry")

        if view.action == "destroy":
            return False

        if view.action == "mark_read":
            return user.is_staff and user.has_perm("inquiries.change_contactinquiry")

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return user.is_staff and user.has_perm("inquiries.view_contactinquiry")

        if view.action == "destroy":
            return False

        if view.action == "mark_read":
            return user.is_staff and user.has_perm("inquiries.change_contactinquiry")

        return False


class ArtworkInquiryPermission(permissions.BasePermission):
    """Permission class for artwork inquiry management."""

    def has_permission(self, request, view):
        user = request.user

        if view.action == "create":
            return True

        if user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return user.is_staff and user.has_perm("inquiries.view_artworkinquiry")

        if view.action == "destroy":
            return False

        if view.action == "mark_read":
            return user.is_staff and user.has_perm("inquiries.change_artworkinquiry")

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return user.is_staff and user.has_perm("inquiries.view_artworkinquiry")

        if view.action == "destroy":
            return False

        if view.action == "mark_read":
            return user.is_staff and user.has_perm("inquiries.change_artworkinquiry")

        return False
