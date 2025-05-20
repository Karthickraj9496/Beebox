from django.contrib import admin
from django.urls import path
from client import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/',views.homepage,name='homepage'),
    path('index/',views.indexpage, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('create/', views.create_booking, name='create_booking'),
    path('booking/', views.booking_list, name='booking_list'),
    path('track/', views.search_booking, name='search_booking'),
]