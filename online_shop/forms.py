from django import forms
from django.forms import ModelForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and validate_email(email):
            raise ValidationError("Enter a valid email address.")
        elif User.objects.filter(email=email).exists():
            raise ValidationError("E-mail: {} already exist!".format(email))
        return email

