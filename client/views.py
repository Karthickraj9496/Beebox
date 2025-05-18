
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking


# Create your views here.
def homepage(request):
    return HttpResponse ('hello world')

def indexpage(request):
    return render(request,'index.html')

# booking view
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return render(request, 'booking_success.html', {'order_id': booking.order_id})
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})



def search_booking(request):
    order_id = request.GET.get('order_id')
    booking = None

    if order_id:
        try:
            booking = Booking.objects.get(order_id=order_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, 'index.html', {'booking': booking})
