from django.shortcuts import render
from .models import Package

def package(request):
    packages = Package.objects.all()
    return render(request, 'package.html', {'packages': packages})