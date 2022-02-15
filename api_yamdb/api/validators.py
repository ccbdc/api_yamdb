from django.core.exceptions import ValidationError
from django.utils import timezone


def time_validator(value):
    if value > timezone.now().year:
        params = {'value': value, }
        raise ValidationError('Enter the current date', params=params)