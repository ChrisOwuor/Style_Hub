from django.db import models

from authentication.models import Stylist

# Create your models here.


class Document(models.Model):
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


class Questionnaire (models.Model):
    question = models.TextField()

    def __str__(self):
        return f"Questionnaire {self.id}"


class UserResponse(models.Model):
    content = models.TextField()
    stylist_id = models.ForeignKey(
        Stylist, on_delete=models.CASCADE, null=True)
    questionnaire_id = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Response by {self.stylist_id.user_name}"
