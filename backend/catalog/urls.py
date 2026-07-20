from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog.views.catalog_views import CatalogViewSet

router = DefaultRouter()
router.register(r"", CatalogViewSet, basename="catalog")

urlpatterns = [
    path("management/", include(router.urls)),
]