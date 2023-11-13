from django.db import models
from django.utils import timezone

class UploadImg(models.Model):
    upload_datetime = models.DateTimeField(default=timezone.now)
    pid = models.IntegerField(null=False)
    patient_name = models.CharField(max_length=100, null=False)
    page = models.IntegerField(null=False)
    brainpics = models.ImageField(upload_to="profiles", blank=False)
    brain_prediction = models.CharField(max_length=30, default='NA')
    brain_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)