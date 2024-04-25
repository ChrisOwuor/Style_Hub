from django.db import models

from authentication.models import Stylist

# Create your models here.


class ApprovalRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    time = models.TimeField()
    date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    stylist_id = models.ForeignKey(Stylist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stylist_id.user_name} - {self.status}"
