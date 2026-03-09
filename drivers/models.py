from datetime import date
from django.core.validators import RegexValidator
from django.db import models
from drivers.validators import driver_years_validator, PhoneNumberValidator


class Driver(models.Model):
    full_name = models.CharField(
        max_length= 50
    )

    date_of_birth = models.DateField(
        validators=[
            driver_years_validator
        ]
    )

    phone_number = models.CharField(
        unique=True,
        validators=[
            PhoneNumberValidator(
                10,
                'Phone number must be exactly 10 digits.',
                'Phone number must contain digits only'
            )
        ]
    )

    photo = models.URLField(
        blank=True,
        null=True
    )

    driving_license_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(r'^[A-Z0-9]{10}$',
                           "Driving Licence must contain exactly 10 uppercase alphanumeric characters")
        ],
        unique=True
    )

    years_of_experience = models.PositiveSmallIntegerField()

    specializations = models.ManyToManyField(
        'Specialization',
        related_name='drivers',
        blank=True
    )

    @property
    def driver_age(self):
        current_year = date.today().year
        return current_year - self.date_of_birth.year

    def __str__(self):
        return f'{self.full_name} - {self.driver_age} years old with {self.years_of_experience} years experience'

class Specialization(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )


    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name