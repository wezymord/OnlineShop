from django.core.exceptions import ValidationError


def clean_first_name(first_name):
    if not first_name.isalpha():
        raise ValidationError("Only alphanumeric characters are allowed.")
    return first_name

def clean_last_name(last_name):
    if not last_name.isalpha():
        raise ValidationError("Only alphanumeric characters are allowed.")
    return last_name
