import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import ClassBooking, ClassProgram, StudioClass
from .serializers import (
    ClassBookingSerializer,
    ClassBookingStatusSerializer,
    CreateClassBookingSerializer,
    StudioClassSerializer,
)
from .services.class_services import ClassService

logger = logging.getLogger(__name__)


class PublicThrottle(AnonRateThrottle):
    scope = "inquiry"


@extend_schema_view(
    list=extend_schema(
        summary="List Studio Classes",
        description="List all active studio classes and their programs.",
    ),
    retrieve=extend_schema(
        summary="Retrieve Studio Class",
        description="Get a single studio class and its active programs.",
    ),
)
class StudioClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudioClass.objects.filter(is_active=True).prefetch_related("programs")
    serializer_class = StudioClassSerializer

    def get_queryset(self):
        return StudioClass.objects.active().prefetch_related("programs")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"classes": serializer.data})

    def retrieve(self, request, pk=None, *args, **kwargs):
        studio_class = self.get_object()
        serializer = self.get_serializer(studio_class)
        return Response({"class": serializer.data})


@extend_schema_view(
    create=extend_schema(
        summary="Create Class Booking",
        description="Submit a new booking for a selected class program.",
    )
)
class ClassBookingViewSet(viewsets.GenericViewSet):
    queryset = ClassBooking.objects.select_related("program").all()
    throttle_classes = [PublicThrottle]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateClassBookingSerializer
        if self.action == "mark_read":
            return ClassBookingStatusSerializer
        return ClassBookingSerializer

    def get_permissions(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = CreateClassBookingSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        program_id = serializer.validated_data.pop("program_id")
        program = ClassProgram.objects.get(pk=program_id)
        booking = ClassService.create_class_booking(
            program=program, validated_data=serializer.validated_data
        )

        return Response(
            {"class_booking": ClassBookingSerializer(booking).data},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        booking = self.get_object()
        serializer = ClassBookingSerializer(booking)
        return Response({"class_booking": serializer.data})
