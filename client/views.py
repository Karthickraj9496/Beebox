
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm,CityForm
from .models import Booking,City
from django.template.loader import render_to_string


# Create your views here.
def homepage(request):
    return HttpResponse ('hello world')

def indexpage(request):
    return render(request,'index.html')

# booking view
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Now this will be a valid User instance
            booking.save()
            return render(request, 'booking_success.html', {'order_id': booking.order_id})
        else:
            return render(request, 'booking_form.html', {'form': form})
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def booking_success(request, order_id):
    return render(request, 'booking_success.html', {'order_id': order_id})

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