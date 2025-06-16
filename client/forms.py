from django import forms
from .models import Booking, City, VehicleType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    