"""
Custom manager for Catalog model with queryset helpers for visibility and ownership scoping.

This module provides CatalogManager which extends models.Manager to implement:

- Visibility Scoping: Explicit helpers for each visibility state (published, draft, archived).
  Default queryset returns ALL catalogs — callers choose the right scope.
- Ownership Scoping: for_user() to scope to a specific user's catalogs.
- Combined Scoping: active_for_user() for published catalogs owned by a specific user.

Default Queryset Behavior:
- objects.all()            → all catalogs regardless of visibility
- objects.published()      → only published catalogs
- objects.draft()          → only draft catalogs
- objects.archived()       → only archived catalogs
- objects.for_user(user)   → all catalogs belonging to a specific user
- objects.published_for_user(user) → published catalogs for a specific user

Design mirrors the UserManager pattern:
- Safe by default (no hidden filtering magic in get_queryset)
- Explicit, named helpers for every common access pattern
- Documented return types and use cases

Dependencies:
- django.db.models.Manager: Base manager class
"""

from django.db import models


class CatalogManager(models.Manager):
    """Manager for Catalog model with visibility-scoped and ownership-scoped querysets."""

    use_in_migrations = True

    def get_queryset(self):
        """Return default queryset — all catalogs regardless of visibility status.

        Does NOT filter by visibility. Use the scoped helpers (published, draft,
        archived) or combine them when you need to filter by visibility status.

        Returns:
            QuerySet of all Catalog objects

        Examples:
            Catalog.objects.all()           # All catalogs
            Catalog.objects.published()     # Only published
            Catalog.objects.for_user(user)  # All catalogs for a user
        """
        return super().get_queryset()

    def published(self):
        """Return only published catalogs.

        Use for public-facing endpoints where only live content is relevant.
        Callers should not need to know the underlying field name or choice value.

        Returns:
            QuerySet[Catalog] filtered to visibility_status='published'

        Use Cases:
            - Public catalog browsing endpoints
            - Search and discovery features
            - External API consumers

        Examples:
            Catalog.objects.published()
            Catalog.objects.published().filter(category='landscapes')
        """
        return self.get_queryset().filter(visibility_status="published")

    def draft(self):
        """Return only draft catalogs.

        Use for staff/owner dashboards showing work-in-progress items.

        Returns:
            QuerySet[Catalog] filtered to visibility_status='draft'

        Use Cases:
            - Staff dashboard showing unpublished work
            - Pre-publication review workflows
            - Owner self-service draft management

        Examples:
            Catalog.objects.draft()
            Catalog.objects.draft().filter(user=request.user)
        """
        return self.get_queryset().filter(visibility_status="draft")

    def archived(self):
        """Return only archived catalogs.

        Use for audit/recovery workflows or admin views of retired content.

        Returns:
            QuerySet[Catalog] filtered to visibility_status='archived'

        Use Cases:
            - Admin audit and compliance reports
            - Recovery workflows for accidentally archived catalogs
            - Historical catalog browsing

        Examples:
            Catalog.objects.archived()
            Catalog.objects.archived().order_by('-updated_at')
        """
        return self.get_queryset().filter(visibility_status="archived")

    def for_user(self, user):
        """Return all catalogs belonging to a specific user, regardless of visibility.

        Use when you need the full set of a user's catalogs (e.g., owner dashboard).
        Combine with .published() or .draft() for narrower scoping.

        Args:
            user: User instance to scope the queryset to.

        Returns:
            QuerySet[Catalog] filtered to the given user across all visibility states.

        Use Cases:
            - Owner self-service catalog management
            - Staff viewing a specific user's catalog portfolio
            - Reporting on a user's total catalog count

        Examples:
            Catalog.objects.for_user(request.user)
            Catalog.objects.for_user(user).filter(visibility_status='draft')
        """
        return self.get_queryset().filter(user=user)

    def published_for_user(self, user):
        """Return only published catalogs belonging to a specific user.

        Convenience combinator for the common pattern of scoping published
        content to a specific owner. Useful for public-facing artist portfolio pages.

        Args:
            user: User instance to scope the queryset to.

        Returns:
            QuerySet[Catalog] filtered to visibility_status='published' and the given user.

        Use Cases:
            - Public-facing artist portfolio page
            - Featured catalog sections scoped to an artist
            - Counting a user's published work

        Examples:
            Catalog.objects.published_for_user(artist)
        """
        return self.published().filter(user=user)


