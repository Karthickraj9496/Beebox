
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm,CityForm
from .models import Booking,City
from django.template.loader import render_to_string

# booking view
from django.contrib import messages
from django.db import transaction  # If using GeoDjango for location
import uuid
from .utils import geocode_address, calculate_estimated_price, assign_driver_to_booking  # your helper funcs



def homepage(request):
    return HttpResponse("hello world" )    

def indexpage(request):
    return render(request, 'index.html') 


@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            pickup_address = form.cleaned_data['pickup_address']
            dropoff_address = form.cleaned_data['delivery_address']
            vehicle_type = form.cleaned_data['vehicle_type']

            try:
                with transaction.atomic():
                    pickup_coords = geocode_address(pickup_address)
                    dropoff_coords = geocode_address(dropoff_address)

                    if not pickup_coords or not dropoff_coords:
                        messages.error(request, 'Failed to geocode addresses.')
                        return render(request, 'booking_form.html', {'form': form})

                    estimate = calculate_estimated_price(
                        pickup_lat=pickup_coords['lat'],
                        pickup_lng=pickup_coords['lng'],
                        dropoff_lat=dropoff_coords['lat'],
                        dropoff_lng=dropoff_coords['lng'],
                        vehicle_type=vehicle_type
                    )

                    booking = Booking.objects.create(
                        user=request.user,
                        pickup_address=pickup_address,
                        delivery_address=dropoff_address,
                        goods_type=form.cleaned_data['goods_type'],
                        weight=form.cleaned_data['weight'],
                        dimensions=form.cleaned_data['dimensions'],
                        phone_no=form.cleaned_data['phone_no'],
                        # vehicle_type=vehicle_type,
                        pickup_latitude=pickup_coords['lat'],
                        pickup_longitude=pickup_coords['lng'],
                        dropoff_latitude=dropoff_coords['lat'],
                        dropoff_longitude=dropoff_coords['lng'],
                        distance_km=estimate['distance_km'],
                        estimated_time_min=estimate['travel_time_min'],
                        price=estimate['estimated_price'],
                        status='pending'
                    )

                    messages.success(request, 'Booking created successfully!')
                    return redirect('booking_detail', booking_id=booking.id)

            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, 'An error occurred during booking.')

    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})

@login_required
def booking_view(request):
    city_name = request.GET.get('city', 'default_city')
    city = get_object_or_404(City, name=city_name)
    form = BookingForm(initial={'city': city})
    return render(request, 'booking_form.html', {'form': form, 'city': city})

def search_booking(request):
    order_id = request.GET.get('order_id')
    booking = None

    if order_id:
        try:
            booking = Booking.objects.get(order_id=order_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, 'index.html', {
        'booking': booking,
        'order_id': order_id
    })



def booking_city(request):
    form = CityForm()
    cities = City.objects.all()
    selected_city = None

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            selected_city = form.cleaned_data['city']

    return render(request, 'booking_form.html', {
        'form': form,
        'cities': cities,
        'selected_city': selected_city,
    })