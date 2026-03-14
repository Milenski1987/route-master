from django.core.validators import RegexValidator
from django.db import models
from common.validators import PhotoURLValidate
from vehicles.choices import VehicleTypeChoices


class Vehicle(models.Model):
    registration_number = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^[A-Z0-9]{6,8}$',
                           "Registration Number must contain between 6 to 8 uppercase alphanumeric characters")
        ],
        unique=True
    )

    make = models.CharField(
        max_length=30
    )

    model = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    photo = models.URLField(
        blank=True,
        null=True,
        validators=[
            PhotoURLValidate('URL must point to a valid image file (.jpg, .jpeg, .png, .gif, .webp)')
        ]
    )

    vehicle_type = models.CharField(
        max_length= 10,
        choices=VehicleTypeChoices.choices
    )

    capacity_kg = models.PositiveIntegerField()

    manufacture_date = models.DateField()

    def __str__(self):
        return f'{self.make} {self.model}'



