"""
Test for my models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from freezegun import freeze_time
import datetime

from core import models


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successfuly(self):
        """Test create a user with an email is successful"""
        email = 'Test@example.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test email is normalised for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test3@EXAMPLE.com', 'test3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'password123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that raises a ValueError if a user tries
        creating a user without an email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @freeze_time("2024-01-01")
    def test_create_booking(self):
        """Test creating a booking"""
        user = get_user_model().objects.create_user(
            email='Test@example.com', password='password123'
        )

        booking = models.Bookings.objects.create(
            user=user,
            start_time=datetime.datetime.now(),
            notes='Test notes',
        )

        self.assertEqual(booking.booking_id, 1)
        self.assertFalse(booking.cancelled)
        self.assertFalse(booking.completed)

    def test_create_service(self):
        """Test creating a service"""
        service = models.BeautyServices.objects.create(
            name='Eyebrow Waxing',
            cost=10.00,
            description='Waxing of the eyebrows',
            service_type='BROWS',
            duration=datetime.timedelta(minutes=30),
        )

        self.assertEqual(str(service), service.name)
