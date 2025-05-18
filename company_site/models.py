from django.db import models

class Package(models.Model):
    tracking_id = models.CharField(max_length=100, unique=True)
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    delivery_date = models.DateField(null=True, blank=True)
