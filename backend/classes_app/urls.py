from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClassBookingViewSet, StudioClassViewSet

router = DefaultRouter()
router.register(r"", StudioClassViewSet, basename="classes")
router.register(r"bookings/v1", ClassBookingViewSet, basename="class-bookings")

urlpatterns = [
    path("", include(router.urls)),
]
