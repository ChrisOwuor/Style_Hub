import uuid
import random
from django.db import models
from django.utils import timezone
from django.conf import settings

from authentication.models import Client, Stylist, User
from stylist.models import Style
# Create your models here.


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)
    style_id = models.ForeignKey(Style, on_delete=models.CASCADE)
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while Booking.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while Transaction.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Transaction ID: {self.id}, Booking ID: {self.booking.id}, Status: {self.status}'




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


class Questionnaire (models.Model):
    question = models.TextField()

    def __str__(self):
        return f"Questionnaire {self.id}"


class StylistResponse(models.Model):
    content = models.TextField()
    stylist_id = models.ForeignKey(
        Stylist, on_delete=models.CASCADE, null=True)
    questionnaire_id = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Response by {self.stylist_id.user_name}"
