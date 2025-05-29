from django import forms
from .models import Booking, City, VehicleType

class BookingForm(forms.ModelForm):
    class Meta:
       model = Booking
       fields = [
            'pickup_address',
            'delivery_address',
            'goods_type',
            'weight',
            'dimensions',
            'phone_no',
            'vehicle_type',
        ]
       widgets = {
            'pickup_address': forms.Textarea(attrs={'rows': 2}),
            'delivery_address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_type'].queryset = VehicleType.objects.all()

class CityForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="-- Choose a city --")
