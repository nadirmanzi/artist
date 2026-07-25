import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view

from inquiries.models import ContactInquiry
from inquiries.serializers import (
    ContactInquirySerializer,
    CreateContactInquirySerializer,
    ContactInquiryStatusSerializer,
)
from inquiries.utils.permissions import ContactInquiryPermission
from inquiries.services.inquiry_services import ContactInquiryService


logger = logging.getLogger(__name__)


class InquiryThrottle(AnonRateThrottle):
    scope = "inquiry"


@extend_schema_view(
    create=extend_schema(
        summary="Create Contact Inquiry",
        description="Submit a new contact inquiry (public).",
    ),
    list=extend_schema(
        summary="List Contact Inquiries",
        description="List all contact inquiries (staff only).",
    ),
    retrieve=extend_schema(
        summary="Retrieve Contact Inquiry",
        description="Get a specific contact inquiry's details.",
    ),
    destroy=extend_schema(
        summary="Delete Contact Inquiry",
        description="Permanently delete a contact inquiry (superusers only).",
    ),
)
class ContactInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for ContactInquiry CRUD."""

    http_method_names = ["get", "post", "delete", "head", "options"]
    throttle_classes = [InquiryThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (
            user.is_staff and user.has_perm("inquiries.view_contactinquiry")
        ):
            return ContactInquiry.objects.all()
        return ContactInquiry.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateContactInquirySerializer
        if self.action == "mark_read":
            return ContactInquiryStatusSerializer
        return ContactInquirySerializer

    def get_permissions(self):
        return [ContactInquiryPermission()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ContactInquirySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ContactInquirySerializer(queryset, many=True)
        return Response({"contact_inquiries": serializer.data})

    def retrieve(self, request, pk=None, *args, **kwargs):
        inquiry = self.get_object()
        serializer = ContactInquirySerializer(inquiry)
        return Response({"contact_inquiry": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = CreateContactInquirySerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        inquiry = ContactInquiryService.create_contact_inquiry(
            validated_data=serializer.validated_data
        )

        return Response(
            {"contact_inquiry": ContactInquirySerializer(inquiry).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        inquiry = self.get_object()
        ContactInquiryService.delete_contact_inquiry(inquiry)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Mark Contact Inquiry as Read",
        description="Mark a contact inquiry as read (requires change_contactinquiry perm).",
    )
    @action(detail=True, methods=["post"], url_path="mark-read")
    def mark_read(self, request, pk=None):
        inquiry = self.get_object()
        inquiry = ContactInquiryService.mark_as_read(inquiry)

        return Response(
            {
                "is_read": inquiry.is_read,
                "contact_inquiry": ContactInquiryStatusSerializer(inquiry).data,
            },
            status=status.HTTP_200_OK,
        )
