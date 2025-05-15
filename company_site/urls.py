from django.contrib import admin
from django.urls import path
from company_site import views

urlpatterns = [
     path('booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
]