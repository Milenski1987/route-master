from datetime import date
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def driver_years_validator(value: int) -> None:
    current_date = date.today()
    driver_bday = value
    age = current_date.year - driver_bday.year

    if (current_date.month < driver_bday.month) or (current_date.month == driver_bday.month and current_date.day < driver_bday.day):
        age -= 1

    if age < 18:
        raise ValidationError("Driver must be at least 18 years old!")


@deconstructible
class PhoneNumberValidator:
    def __init__(self, length: int, length_message: str, contain_message: str) -> None:
        self.length = length
        self.length_message = length_message
        self.contain_message = contain_message

    def __call__(self, value: str) -> None:
        if len(value) != self.length:
            raise ValidationError(self.length_message)

        if not value.isdigit():
            raise ValidationError(self.contain_message)