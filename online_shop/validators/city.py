from django.core.exceptions import ValidationError


def clean_city(city):
    if not city.isalpha():
        raise ValidationError("Only alphanumeric characters are allowed.")
    return city