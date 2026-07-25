from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inquiries.views.contact_inquiry_views import ContactInquiryViewSet
from inquiries.views.artwork_inquiry_views import ArtworkInquiryViewSet

router = DefaultRouter()
router.register(r"contact", ContactInquiryViewSet, basename="contact-inquiries")
router.register(r"artwork", ArtworkInquiryViewSet, basename="artwork-inquiries")

urlpatterns = [
    path("", include(router.urls)),
]
