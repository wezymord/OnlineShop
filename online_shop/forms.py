from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
from django_countries import countries
from .validators.postal_code import postal_code_validate
from .validators.e_mail import clean_email
import re


class ProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-fn'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-ln'}))
    email = forms.EmailField(validators=[clean_email], widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-company'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-city'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-zip'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address1'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address2'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company',
                  'country', 'city', 'postal_code', 'address1', 'address2',]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-phone'}),
            'country': forms.Select(choices=countries, attrs={'class': 'form-control', 'id': 'checkout-country'}),
        }

    def clean_postal_code(self):
        country_code = self.cleaned_data['country']
        postal_code = self.cleaned_data['postal_code']
        if not re.match(postal_code_validate(country_code), postal_code):
            raise ValidationError("Enter postal code appropriate for your country.")
        return country_code