"""
Views for the Booking API
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Booking
from booking import serializers


class BookingViewSet(viewsets.ModelViewSet):
    """Manage Booking in the database"""

    serializer_class = serializers.BookingSerializer
    queryset = Booking.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by(
            '-booking_id'
        )

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new booking"""
        serializer.save(user=self.request.user)
