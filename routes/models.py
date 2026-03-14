from django.db import models
from common.mixins import TimeStampMixin


class DeliveryPoint(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    address = models.CharField(
        max_length=150
    )

    city = models.CharField(
        max_length=30
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} - {self.city}'


class Route(TimeStampMixin):
    name = models.CharField(
        max_length= 30
    )

    start_location = models.CharField(
        max_length=30
    )

    end_location = models.CharField(
        max_length=30
    )

    distance_km = models.PositiveIntegerField()

    points_for_delivery = models.ManyToManyField(
        'DeliveryPoint',
        related_name='delivery_point_routes',
        blank=True
    )

    def __str__(self):
        return f'{self.start_location} - {self.end_location}'


class Assignment(TimeStampMixin):
    route = models.ForeignKey(
        'Route',
        on_delete=models.PROTECT,
        related_name='route_assignments'
    )

    driver = models.ForeignKey(
        'drivers.Driver',
        on_delete=models.PROTECT,
        related_name='driver_assignments'
    )

    vehicle = models.ForeignKey(
        'vehicles.Vehicle',
        on_delete=models.PROTECT,
        related_name='vehicle_assignments'
    )

    assignment_start = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True
    )