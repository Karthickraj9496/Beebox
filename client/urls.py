from django.contrib import admin
from django.urls import path
from client import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/',views.homepage,name='homepage'),
    path('about/',views.about,name='about'),
    path('service/',views.ourservice,name='service'),
    path('index/',views.indexpage, name='index'),
    path('track/',views.track, name='track'),
    path('success/',views.booking_success, name='success'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.registers, name='signup'),
    path('create/', views.create_booking, name='create_booking'),
    path('booking/', views.booking_list, name='booking_list'),
    path('search/', views.search_booking, name='search_booking'),
    # path('city/', views.booking_view, name='city'),
]