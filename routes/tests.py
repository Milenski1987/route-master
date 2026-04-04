from datetime import date, timedelta
from django.test import TestCase
from drivers.models import Driver
from vehicles.models import Vehicle
from vehicles.choices import VehicleTypeChoices
from routes.models import Route, Assignment
from routes.forms import AssignmentAddForm


class AssignmentFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            full_name='Milen Nikolov',
            date_of_birth=date(1987, 7, 30),
            phone_number='0887356155',
            driving_license_number='MN12121212',
            years_of_experience=15,
        )

        self.vehicle = Vehicle.objects.create(
            registration_number='CA1987CA',
            make='Mercedes',
            vehicle_type=VehicleTypeChoices.choices[0][0],
            capacity_kg=1000,
            manufacture_date=date(2020, 2, 20),
        )

        self.route = Route.objects.create(
            name='Sofia - Plovidiv',
            start_location='Sofia',
            end_location='Plovdiv',
            distance_km=150,
        )

    def test_assignment_add__with_valid_data__expect_form_passes(self):
        form = AssignmentAddForm(data={
            'route': self.route.pk,
            'driver': self.driver.pk,
            'vehicle': self.vehicle.pk,
            'assignment_start': date.today() + timedelta(days=1),
        })

        self.assertTrue(form.is_valid())

    def test_assignment_add__with_past_date__expect_form_raises_error(self):
        form = AssignmentAddForm(data={
            'route': self.route.pk,
            'driver': self.driver.pk,
            'vehicle': self.vehicle.pk,
            'assignment_start': date.today() - timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('assignment_start', form.errors)

    def test_assignment_add__with_unavailable_driver_for_that_date__expect_form_raises_error(self):
        Assignment.objects.create(
            route=self.route,
            driver=self.driver,
            vehicle=self.vehicle,
            assignment_start=date.today() + timedelta(days=1),
        )

        other_vehicle = Vehicle.objects.create(
            registration_number='CA2020CA',
            make='Scania',
            vehicle_type=VehicleTypeChoices.choices[0][0],
            capacity_kg=1200,
            manufacture_date=date(2020, 6, 25),
        )

        form = AssignmentAddForm(data={
            'route': self.route.pk,
            'driver': self.driver.pk,
            'vehicle': other_vehicle.pk,
            'assignment_start': date.today() + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('driver', form.errors)


    def test_assignment_add__with_unavailable_vehicle_for_that_date__expect_form_raises_error(self):
        Assignment.objects.create(
            route=self.route,
            driver=self.driver,
            vehicle=self.vehicle,
            assignment_start=date.today() + timedelta(days=1),
        )

        other_driver = Driver.objects.create(
            full_name='Milena Nikolova',
            date_of_birth=date(1989, 8, 21),
            phone_number='0887356158',
            driving_license_number='MN13131313',
            years_of_experience=13,
        )

        form = AssignmentAddForm(data={
            'route': self.route.pk,
            'driver': other_driver.pk,
            'vehicle': self.vehicle.pk,
            'assignment_start': date.today() + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('vehicle', form.errors)