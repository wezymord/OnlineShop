from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("E-mail: {} already exist!".format(email))
        return email