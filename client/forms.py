from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_address', 'delivery_address', 'goods_type', 'weight', 'dimensions', 'phone_no']
        labels = {'weight':'kg'}
        help_text = {'pickup_address':'please enter the correct address','delivery_address':'please enter the correct address'}
        
