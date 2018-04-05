from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email


def email_validator(user_email, logged_email=''):
    if user_email and validate_email(user_email):
        raise ValidationError("Enter a valid email address.")
    elif logged_email != user_email:
        if User.objects.filter(email=user_email).exists():
            raise ValidationError("E-mail: {} already exist!".format(user_email))
    return user_email