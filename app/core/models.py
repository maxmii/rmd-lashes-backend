"""
Models for database
"""

import datetime
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user"""
        if not email:
            raise ValueError('Email must be provided')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    booking_starttime = models.DateTimeField(
        validators=[MinValueValidator(datetime.datetime.now())]
    )
    booking_endtime = models.DateTimeField(
        validators=[MinValueValidator(datetime.datetime.now())]
    )
    booking_duration = models.DurationField()
    booking_duration = models.DurationField()
    booking_notes = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    booking_cancelled = models.BooleanField(default=False)
    booking_completed = models.BooleanField(default=False)
    service_id = models.ForeignKey('Services', on_delete=models.CASCADE)


class Services(models.Model):
    SERVICE_CHOICES = {
        "LASHES": "Lashes",
        "NAILS": "Nails",
        "BROWS": "Brows",
    }
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255)
    service_desciption = models.TextField(blank=True)
    service_duration = models.DurationField()
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(choices=SERVICE_CHOICES)

    def __str__(self):
        """Return service name"""
        return self.service_name
