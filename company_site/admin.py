from django.contrib import admin
from .models import Package,Dealer, Driver, Book

# Register your models here.
admin.site.register(Package)
admin.site.register(Dealer)
admin.site.register(Driver)
admin.site.register(Book)