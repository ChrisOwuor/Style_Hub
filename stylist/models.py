from django.db import models
from authentication.models import Stylist
import uuid


# Create your models here.


class StylistDocument(models.Model):
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="Media/")
    national_id_front = models.ImageField(
        null=True, blank=True, upload_to="Media/")
    national_id_back = models.ImageField(
        null=True, blank=True, upload_to="Media/")
    good_conduct_cert = models.ImageField(
        null=True, blank=True, upload_to="Media/")
    stylist_id = models.ForeignKey(
        Stylist, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Document for {self.stylist_id.user_name}"


class StyleCategorie(models.Model):
    category_name = models.CharField(max_length=100)
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while StyleCategorie.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Style(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to="Media/")
    category = models.ForeignKey(StyleCategorie, on_delete=models.CASCADE)
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while Style.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StyleVariation(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=4, max_digits=12)
    photo = models.ImageField(null=True, blank=True, upload_to="Media/")
    video = models.ImageField(null=True, blank=True, upload_to="Media/")
    length = models.DecimalField(decimal_places=4, max_digits=12)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    u_id = models.UUIDField(editable=False, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while StyleVariation.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
