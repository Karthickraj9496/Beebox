from django import forms
from .models import Booking,City

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_address', 'delivery_address', 'goods_type', 'weight', 'dimensions', 'phone_no']
        labels = {'weight':'kg'}
        help_texts = {'pickup_address':'please enter the correct address','delivery_address':'please enter the correct address'}
        widgets = {
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Address'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Delivery Address'}),
            'goods_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of Goods'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 20x30x15 cm'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class CitySelectionForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select a City")
