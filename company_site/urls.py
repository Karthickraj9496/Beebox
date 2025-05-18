from django.contrib import admin
from django.urls import path
from company_site import views

urlpatterns = [
     path('packages/', views.package, name='package_list'),
]