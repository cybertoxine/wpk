from django.db import models

class Document(models.Model):
    pacjent = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=False)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Dopacjenta(models.Model):
    pacjent = models.CharField(max_length=255, blank=False)
    message = models.TextField(blank=False)
    contact = models.CharField(max_length=255, blank=True)
    date_send = models.DateTimeField(auto_now_add=True)