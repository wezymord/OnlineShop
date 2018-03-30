from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ProfileUserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-fn'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-ln'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-phone'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-company'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-country'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-city'}))
    postal_code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-zip'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address1'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address2'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        if email and validate_email(email):
            raise ValidationError("Enter a valid email address.")
        elif User.objects.filter(email=email).exists():
            raise ValidationError("E-mail: {} already exist!".format(email))
        return email