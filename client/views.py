
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm,CityForm
from .models import Booking,City
from django.template.loader import render_to_string
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
# booking view
from django.contrib import messages
from django.db import transaction  # If using GeoDjango for location
import uuid
from .utils import geocode_address, calculate_estimated_price, assign_driver_to_booking  # your helper funcs
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# live
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from client.models import Booking

# List all bookings
# Booking.objects.filter(id=1).exists()
# print(bookings)
# for b in bookings:
#     print("ID:", b.id)
#     print("User:", b.user)
#     print("Status:", b.status)
#     print("Pickup Address:", b.pickup_address)
#     print("Price:", b.price)
#     print("---")

def homepage(request):
    return HttpResponse("hello world")    

def about(request):
    return render(request,'about.html')

def ourservice(request):
    return render(request,'service.html')

def indexpage(request):
    return render(request, 'index.html') 

@login_required
def create_booking(request):
    selected_city = None
    city_form = CityForm()
    booking_form = BookingForm()

    if request.method == 'POST':
        if 'city' in request.POST:
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                selected_city = city_form.cleaned_data['city']
        else:
            booking_form = BookingForm(request.POST)
            city_form = CityForm()  # Reset city form

            if booking_form.is_valid():
                try:
                    pickup_address = booking_form.cleaned_data['pickup_address']
                    dropoff_address = booking_form.cleaned_data['delivery_address']
                    vehicle_type = booking_form.cleaned_data['vehicle_type']

                    # Geocode both addresses
                    pickup_coords = geocode_address(pickup_address)
                    dropoff_coords = geocode_address(dropoff_address)

                    if not pickup_coords or not dropoff_coords:
                        messages.error(request, 'Failed to geocode addresses.')
                        return render(request, 'booking_form.html', {
                            'booking_form': booking_form,
                            'city_form': city_form,
                            'selected_city': selected_city
                        })

                    # Estimate price and travel time
                    estimate = calculate_estimated_price(
                        pickup_lat=pickup_coords['lat'],
                        pickup_lng=pickup_coords['lng'],
                        dropoff_lat=dropoff_coords['lat'],
                        dropoff_lng=dropoff_coords['lng'],
                        vehicle_type=vehicle_type
                    )

                    with transaction.atomic():
                        booking = booking_form.save(commit=False)
                        booking.user = request.user
                        booking.pickup_latitude = pickup_coords['lat']
                        booking.pickup_longitude = pickup_coords['lng']
                        booking.dropoff_latitude = dropoff_coords['lat']
                        booking.dropoff_longitude = dropoff_coords['lng']
                        booking.distance_km = estimate['distance_km']
                        booking.estimated_time_min = estimate['travel_time_min']
                        booking.price = estimate['estimated_price']
                        booking.status = 'pending'
                        booking.save()

                        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                        razorpay_order = client.order.create({
                            'amount': int(booking.price * 100),  # price in paise
                            'currency': 'INR',
                            'payment_capture': 1
                        })

                        booking.razorpay_order_id = razorpay_order['id']
                        booking.save()

                    # ✅ Render payment page
                    return render(request, 'payment_page.html', {
                        'order_id': razorpay_order['id'],
                        'key_id': settings.RAZORPAY_KEY_ID,
                        'amount': int(booking.price * 1),
                        'display_amount': booking.price,
                        'booking': booking
                    })

                        
                    # messages.success(request, "Booking created successfully!")
                    # return render(request, 'booking_success.html', {'order_id': booking.order_id})
                    # # return redirect('booking_detail')  # or render booking_success.html

                except Exception as e:
                    print(f"Booking error: {e}")
                    messages.error(request, 'An error occurred during booking. Please try again.')
            else:
                messages.error(request, "Please correct the form errors.")

    return render(request, 'booking_form.html', {
        'booking_form': booking_form,
        'city_form': city_form,
        'selected_city': selected_city
    })

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking_list.html', {'bookings': bookings})
    
@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_detail.html', {'booking': booking})

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user) 
#             return redirect('login')  
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


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

def track(request):
    order_id = request.GET.get('order_id')
    booking = None

    if order_id:
        try:
            booking = Booking.objects.get(order_id=order_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, 'track.html', {
        'booking': booking,
        'order_id': order_id
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('home')  # replace with your homepage or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def registers(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, "signup.html")

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login') 

@csrf_exempt
def payment_handler(request):

    if request.method == "POST":
        try:
            # get the required parameters from POST request
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # verify the payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = client.utility.verify_payment_signature(params_dict)

            if result is None:
                # payment successful
                # here you can update booking in DB to mark as paid
                booking = Booking.objects.get(razorpay_order_id=order_id)
                booking.status = 'paid'
                booking.save()

                # Optionally pass details to template
                return render(request, 'success.html', {
                    'booking': booking,
                    'payment_id': payment_id
                })
            else:
                # Signature verification failed
                return render(request, 'failed.html')

        except Exception as e:
            print(f"Payment verification error: {e}")
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def update_vehicle_location(request, booking_id):
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        if lat is None or lng is None:
            return JsonResponse({'status': 'error', 'message': 'Missing lat/lng'})
        try:
            lat = float(lat)
            lng = float(lng)
            booking = Booking.objects.get(id=booking_id)

            booking.vehicle_latitude = lat
            booking.vehicle_longitude = lng
            booking.save()
            return JsonResponse({'status': 'success'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Booking not found'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid lat/lng format'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def tracking_page(request, booking_id):
    booking = get_object_or_404(id=booking_id, user=request.user)
    return render(request, 'tracking.html', {'booking': booking})

@login_required
def get_vehicle_location(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        data = {
            'latitude': booking.vehicle_latitude,
            'longitude': booking.vehicle_longitude,
            'status': booking.status,
        }
        return JsonResponse(data)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)

