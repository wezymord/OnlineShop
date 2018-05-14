from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries import countries
from .validators.postal_code import PostalCodeValidator
from .validators.e_mail import email_validator



class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-fn'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-ln'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'}))
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-company'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-city'}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-zip'}))
    address1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address1'}))
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

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not first_name:
            raise forms.ValidationError('The field can not be empty')
        elif not first_name.isalpha():
            raise ValidationError("Only alphanumeric characters are allowed.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not last_name:
            raise forms.ValidationError('The field can not be empty')
        elif not last_name.isalpha():
            raise ValidationError("Only alphanumeric characters are allowed.")
        return last_name

    def clean_email(self):
        user_email = self.cleaned_data['email']

        if not user_email:
            raise forms.ValidationError('The field can not be empty')
        elif self.logged_user_id:
            logged_email = User.objects.get(pk=self.logged_user_id).email
            return email_validator(user_email, logged_email)
        return email_validator(user_email)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if not phone_number:
            raise forms.ValidationError('The field can not be empty')
        return phone_number

    def clean_country(self):
        country = self.cleaned_data['country']

        if not country:
            country += 'error'
            return country

        return country

    def clean_city(self):
        city = self.cleaned_data['city']

        if not city:
            raise forms.ValidationError('The field can not be empty')
        elif not city.isalpha():
            raise ValidationError("Only alphanumeric characters are allowed.")
        return city

    def clean_postal_code(self):
        country_code = self.cleaned_data['country']
        postal_code = self.cleaned_data['postal_code']
        if not postal_code:
            raise forms.ValidationError('The field can not be empty')
        elif country_code == 'error':
            raise forms.ValidationError('First choose the country')
        elif not PostalCodeValidator().is_valid(country_code, postal_code):
            raise ValidationError("Enter postal code appropriate for your country.")
        return postal_code

    def clean_address1(self):
        address1 = self.cleaned_data['address1']

        if not address1:
            raise forms.ValidationError('The field can not be empty')
        return address1


class RegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'reg-pass'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'reg-pass-confirm'}))

    def clean_repeat_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['repeat_password']
        if password1 != password2:
            raise forms.ValidationError("Passwords should be identical.")
        return password1