"""
FilterSet for the Catalog model.

Supports filtering by:
- Text search on name and description (icontains — case-insensitive partial match)
- Exact choice filters: category, visibility_status
- Price range: price_min (>=), price_max (<=)
- Date range: created_at_after (>=), created_at_before (<=)
- Owner: user (by UUID — filters on user__user_id)

Design mirrors UserFilter from the users app — each filter field maps
explicitly to a model lookup expression so behaviour is predictable and
documented.

Usage examples:
    GET /catalog/management/?name=portrait
    GET /catalog/management/?visibility_status=published&price_min=100
    GET /catalog/management/?created_at_after=2025-01-01&category=landscapes
    GET /catalog/management/?user=<uuid>
"""

import django_filters

from .models import Catalog


class CatalogFilter(django_filters.FilterSet):
    """
    FilterSet for the Catalog model.

    Supports filtering by:
    - Text search on name and description (icontains)
    - Exact match: category, visibility_status
    - Price range: price_min, price_max
    - Date range: created_at_after, created_at_before
    - Owner: user (by UUID)
    """

    # Text search filters — case-insensitive partial match
    name = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    medium = django_filters.CharFilter(lookup_expr="icontains")

    # Exact choice filters
    category = django_filters.ChoiceFilter(choices=Catalog.CategoryChoices.choices)
    visibility_status = django_filters.ChoiceFilter(
        choices=Catalog.VisibilityStatus.choices
    )

    # Price range — inclusive lower and upper bounds
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    
    # Exact year filter
    year = django_filters.NumberFilter(field_name="year")

    # Date range — filters on created_at timestamp
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    # Owner filter — UUID of the user who owns the catalog
    user = django_filters.UUIDFilter(field_name="user__user_id")

    class Meta:
        model = Catalog
        fields = [
            "name",
            "description",
            "medium",
            "category",
            "visibility_status",
            "price_min",
            "price_max",
            "year",
            "created_at_after",
            "created_at_before",
            "user",
            "is_sold"
        ]
