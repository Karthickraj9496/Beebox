# client/utils.py

def geocode_address(address):
    # Dummy data for testing
    return {
        'lat': 17.385044,
        'lng': 78.486671
    }

def calculate_estimated_price(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, vehicle_type):
    # Dummy calculation
    return {
        'distance_km': 12.5,
        'travel_time_min': 30,
        'estimated_price': 150.0
    }

def assign_driver_to_booking(booking_id):
    # Simulate background task (replace with actual logic later)
    print(f"Assigning driver to booking {booking_id}")
