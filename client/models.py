from django.db import models
from django.contrib.auth.models import User
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in-transit', 'In-Transit'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    goods_type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    phone_no = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    branch_id = models.CharField(max_length=10,default='vpt1') 
    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        prefix = 'gst000'
        short_uuid = uuid.uuid4().hex[:7].upper()
        return f"{prefix}{self.branch_id}{short_uuid}"
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.status}"
    
class City(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to='city_backgrounds/')
    branch_id = models.IntegerField()

    def __str__(self):
        return self.name



