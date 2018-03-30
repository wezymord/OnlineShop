from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email


def clean_email(email):
    if email and validate_email(email):
        raise ValidationError("Enter a valid email address.")
    elif User.objects.filter(email=email).exists():
        raise ValidationError("E-mail: {} already exist!".format(email))
    return email