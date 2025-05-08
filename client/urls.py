from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [
    path('home/',views.homepage,name='homepage'),
    path('index/',views.indexpage,name='index')
]