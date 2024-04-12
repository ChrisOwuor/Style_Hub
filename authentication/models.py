import os
import random
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.conf import settings


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, full_name,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        superuser = self.create_user(
            email, full_name,  password, **other_fields)
        Admin.objects.create(user=superuser)

        return superuser

    def create_user(self, email, full_name,  password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    img_path = os.path.join(settings.BASE_DIR, 'Media', 'user_icon.jpeg')

    class UserType(models.TextChoices):
        CLIENT = 'client'
        STYLIST = 'stylist'
        ADMIN = 'admin'

    email = models.EmailField(verbose_name=_('email address'), unique=True)
    full_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.CLIENT)
    u_id = models.UUIDField(editable=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while User.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)


class Admin(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return f"Admin: {self.user.full_name}"


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='client_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    residency = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Client: {self.user.full_name}"


class Stylist(models.Model):

    GENDER_CHOICES = [
        ('Male', 'male'),
        ('Female', 'female'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='stylist_profile')
    user_name = models.CharField(max_length=150, default="")
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    residency = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin_name = models.CharField(max_length=255, null=True, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(
        max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=20, null=True, blank=True)
    gender = models.CharField(
        max_length=50, default="Female", choices=GENDER_CHOICES)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Stylist: {self.user.full_name}"


class Otp(models.Model):
    created_for = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=7)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        """get desired mins otp"""
        otp_time_sec = float(settings.OTP_EXPIRE_TIME * 60)
        current_time = timezone.now()
        time_diff = current_time - self.created_at

        return time_diff.total_seconds() <= otp_time_sec

    @classmethod
    def get_code(cls):
        random_number = random.randint(1000, 9999)
        return random_number

    def __str__(self):
        return f"OTP for {self.created_for.full_name}"
