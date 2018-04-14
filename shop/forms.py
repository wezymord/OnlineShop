from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries import countries
from .validators.postal_code import PostalCodeValidator
from .validators.e_mail import email_validator
from .validators.first_last_name import clean_first_name, clean_last_name
from .validators.city import clean_city



class UserForm(forms.ModelForm):
    first_name = forms.CharField(validators=[clean_first_name], widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-fn'}))
    last_name = forms.CharField(validators=[clean_last_name], widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-ln'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'}))
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-company'}))
    city = forms.CharField(validators=[clean_city], widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-city'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-zip'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address1'}))
    address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address2'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company',
                  'country', 'city', 'postal_code', 'address1', 'address2']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-phone'}),
            'country': forms.Select(choices=countries, attrs={'class': 'form-control', 'id': 'checkout-country'}),
        }

    def __init__(self, *args, **kwargs):
        if 'user_id' in kwargs.keys():
            self.logged_user_id = kwargs.pop('user_id')
            super(UserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if self.logged_user_id:
            logged_email = User.objects.get(pk=self.logged_user_id).email
            return email_validator(user_email, logged_email)
        return email_validator(user_email)

    def clean_postal_code(self):
        country_code = self.cleaned_data['country']
        postal_code = self.cleaned_data['postal_code']
        if not PostalCodeValidator().is_valid(country_code, postal_code):
            raise ValidationError("Enter postal code appropriate for your country.")
        return postal_code


class RegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'reg-pass'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'reg-pass-confirm'}))

    def clean_repeat_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['repeat_password']
        if password1 != password2:
            raise forms.ValidationError("Passwords should be identical.")
        return password1