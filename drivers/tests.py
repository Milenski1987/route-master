from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from drivers.validators import driver_years_validator, PhoneNumberValidator


class DriverYearsValidatorTests(TestCase):
    def test_years__with_greater_value__expect_driver_passes(self):
        birthdate = date.today().replace(year=date.today().year - 19)
        driver_years_validator(birthdate)

    def test_years__with_exactly_value__expect_driver_passes(self):
        birthdate = date.today().replace(year=date.today().year - 18)
        driver_years_validator(birthdate)

    def test_years__with_lower_value__expect_error_raises(self):
        birthdate = date.today().replace(year=date.today().year - 17)
        with self.assertRaises(ValidationError):
            driver_years_validator(birthdate)

    def test_years__with_lower_value__expect_error_raises_and_show_message(self):
        birthdate = date.today().replace(year=date.today().year - 17)
        with self.assertRaises(ValidationError) as ve:
            driver_years_validator(birthdate)

        self.assertIn('Driver must be at least 18 years old!', str(ve.exception))


class PhoneNumberValidatorTests(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator(
            10,
            'Phone number must be exactly 10 digits.',
            'Phone number must contain digits only'
        )

    def test_valid_phone_number_expect_phone_passes(self):
        self.validator('0887356155')  # should not raise

    def test_short_phone_number__expect_error_raises(self):
        with self.assertRaises(ValidationError):
            self.validator('088735615')

    def test_long_phone_number__expect_error_raises(self):
        with self.assertRaises(ValidationError):
            self.validator('08873561561')

    def test_non_digit_phone_raises(self):
        with self.assertRaises(ValidationError):
            self.validator('088735615B')

    def test_non_digit_phone_number__expect_raises_error_and_shows_correct_message(self):
        with self.assertRaises(ValidationError) as ve:
            self.validator('088735615B')

        self.assertIn('Phone number must contain digits only', str(ve.exception))