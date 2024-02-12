"""
Tests for the Booking API
"""

from freezegun import freeze_time
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Booking

from booking.serializers import BookingSerializer


BOOKING_URL = reverse('booking:booking-list')


def detail_url(self):
    """Create and return a booking detail URL"""
    return reverse('booking:booking-detail', args=[self.booking_id])


@freeze_time("2024-01-01")
def create_booking(user, **params):
    """Create and return a booking"""
    defaults = {
        'start_time': timezone.now(),
        'notes': 'Test notes',
    }
    defaults.update(params)

    booking = Booking.objects.create(user=user, **defaults)
    return booking


def create_user(**params):
    """Create and return a user"""
    return get_user_model().objects.create_user(**params)


class PublicBookingApiTests(TestCase):
    """Test the public Booking API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that login is required for retrieving bookings"""
        res = self.client.get(BOOKING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookingApiTests(TestCase):
    """Test the private Booking API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_booking_for_user(self):
        """Test retrieving booking for user"""
        create_booking(user=self.user)
        create_booking(user=self.user)

        res = self.client.get(BOOKING_URL)

        booking = Booking.objects.all().order_by('-booking_id')
        serializer = BookingSerializer(booking, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_booking_list_limited_to_user(self):
        """Test that booking returned are for the authenticated user"""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        create_booking(user=other_user)
        create_booking(user=self.user)

        res = self.client.get(BOOKING_URL)

        bookings = Booking.objects.filter(user=self.user)
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
