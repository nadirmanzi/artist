"""
Permission class for catalog management.

Rules (mirrors UserActionPermission from users.utils.permissions):
- Superusers can do anything, including DELETE
- Staff with 'catalog.view_catalog' can list/retrieve
- Staff with 'catalog.add_catalog' can create (catalog auto-assigned to request.user)
- Staff with 'catalog.change_catalog' can update/partial_update and set_draft
- Staff with 'catalog.can_publish_catalog' can publish a catalog
- Staff with 'catalog.can_archive_catalog' can archive a catalog
- ONLY SUPERUSERS can delete a catalog (destroy action)
- All other users (regular, anonymous) are denied ALL access

This class handles both view-level (has_permission) and object-level
(has_object_permission) checks, matching the two-phase permission model
used in UserActionPermission.
"""

from rest_framework import permissions


class CatalogPermission(permissions.BasePermission):
    """
    Permission class for catalog management with action-level restrictions.

    Rules:
    - Superusers can do anything
    - Staff with 'catalog.view_catalog' can list and retrieve
    - Staff with 'catalog.add_catalog' can create (user auto-assigned from request.user)
    - Staff with 'catalog.change_catalog' can update/partial_update and set_draft
    - Staff with 'catalog.can_publish_catalog' can publish
    - Staff with 'catalog.can_archive_catalog' can archive
    - ONLY superusers can DELETE a catalog
    - Regular or unauthenticated users are denied all access
    """

    def has_permission(self, request, view):
        """
        Check view-level permissions (list, create, and all other actions).

        Called before the view and before object retrieval. Handles:
        - Authentication check
        - Superuser passthrough
        - Action-specific permission requirements for staff

        Returns:
            bool: True if user may proceed with the requested action
        """
        user = request.user


        # Superusers can do anything
        if user.is_superuser:
            return True

       
        # Create: requires add_catalog permission
        # Catalog is auto-assigned to request.user — user field is never in request body
        if view.action == "create":
            return user.is_staff and user.has_perm("catalog.add_catalog")

        # Update/partial_update: requires change_catalog permission
        if view.action in ["update", "partial_update"]:
            return user.is_staff and user.has_perm("catalog.change_catalog")

        # Delete: ONLY superusers — already handled above; always deny non-superusers
        if view.action == "destroy":
            return False

        # Publish custom action
        if view.action == "publish":
            return user.is_staff and user.has_perm("catalog.can_publish_catalog")

        # Archive custom action
        if view.action == "archive":
            return user.is_staff and user.has_perm("catalog.can_archive_catalog")

        # Set draft custom action: reverting visibility requires change_catalog
        if view.action == "set_draft":
            return user.is_staff and user.has_perm("catalog.change_catalog")

        # Default deny for unknown/unrecognized actions
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions on a specific catalog instance.

        Called after the object is retrieved from the database. Provides a
        second layer of enforcement so permissions are consistent even if
        the view bypasses has_permission.

        Returns:
            bool: True if user may perform the action on this specific catalog
        """
        user = request.user

        # Superusers can do anything
        if user.is_superuser:
            return True

        # Write methods — check specific permission per action
        if view.action in ["update", "partial_update"]:
            return user.is_staff and user.has_perm("catalog.change_catalog")

        # Delete: ONLY superusers — already blocked at view level for non-superusers
        if view.action == "destroy":
            return False

        if view.action == "publish":
            return user.is_staff and user.has_perm("catalog.can_publish_catalog")

        if view.action == "archive":
            return user.is_staff and user.has_perm("catalog.can_archive_catalog")

        if view.action == "set_draft":
            return user.is_staff and user.has_perm("catalog.change_catalog")

        # Default deny for unknown/unrecognized actions
        return False