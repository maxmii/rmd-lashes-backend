"""
Serializers for Booking API
"""

from rest_framework import serializers

from core.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for booking objects"""

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'start_time',
            'notes',
            'created_at',
            'cancelled',
            'completed',
            'beauty_services',
        ]
        read_only_fields = ['booking_id']
