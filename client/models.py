from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class VehicleType(models.Model):
    type_name = models.CharField(max_length=100,unique=True)
    capacity = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class Booking(models.Model):
    class Meta:
        ordering = ['-booking_date']
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in-transit', 'In-Transit'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    goods_type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    phone_no = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    branch_id = models.CharField(max_length=10, default='vpt1') 
    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)
    # Driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_latitude = models.FloatField(null=True, blank=True)
    vehicle_longitude = models.FloatField(null=True, blank=True)
    vehicle_type = models.ForeignKey(
    'VehicleType',
    on_delete=models.SET_NULL,
    related_name='bookings',
    null=True,
    blank=True
)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_time_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)
        
    def generate_order_id(self):
        prefix = 'G2T'
        return f"{prefix}-{self.branch_id}-{uuid.uuid4().hex[:8].upper()}"
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.status}"

class City(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to='city_backgrounds/')
    branch_id = models.IntegerField()

    def __str__(self):
        return self.name

# class cold(models.model):
#     name = models.charField(max_length=100)
#     amount = models.charfirld

