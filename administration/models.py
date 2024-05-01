from django.db import models
import uuid
from authentication.models import Stylist


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
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while ApprovalRequest.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stylist_id.user_name} - {self.status}"
