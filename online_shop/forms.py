from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("E-mail: {} already exist!".format(email))
        elif email and validate_email(email):
            raise ValidationError("Enter a valid email address.")
        return email