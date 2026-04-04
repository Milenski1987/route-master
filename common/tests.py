from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from common.validators import PhotoURLValidate


class AccessControlTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            employee_id='100000',
            first_name='Milen',
            last_name='Nikolov',
            email='m.nikolov@routemaster.com',
            password='P0werPass',
        )

    def test_access_homepage__with_unauthenticated_user__expect_passes(self):
        response = self.client.get(reverse('common:home'))
        self.assertEqual(response.status_code, 200)

    def test_access_login_page__with_unauthenticated_user__expect_passes(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_access_register_page__with_unauthenticated_user__expect_passes(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_acces_driver_list__with_unauthenticated_user__expect_redirect(self):
        response = self.client.get(reverse('driver:list'))
        self.assertEqual(response.status_code, 302)

    def test_acces_driver_list__with_authenticated_user__expect_passes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('driver:list'))
        self.assertEqual(response.status_code, 200)

    def test_access_vehicle_list__with_unauthenticated_user__expect_redirect(self):
        response = self.client.get(reverse('vehicle:list'))
        self.assertEqual(response.status_code, 302)

    def test_acces_vehicle_list__with_authenticated_user__expect_passes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('vehicle:list'))
        self.assertEqual(response.status_code, 200)

    def test_access_routes_list__with_unauthenticated_user__expect_redirect(self):
        response = self.client.get(reverse('routes:routes_list'))
        self.assertEqual(response.status_code, 302)

    def test_acces_routes_list__with_authenticated_user__expect_passes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('routes:routes_list'))
        self.assertEqual(response.status_code, 200)

    def test_access_assignments_list__with_unauthenticated_user__expect_redirect(self):
        response = self.client.get(reverse('routes:assignment_list'))
        self.assertEqual(response.status_code, 302)

    def test_acces_assignments_list__with_authenticated_user__expect_passes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('routes:assignment_list'))
        self.assertEqual(response.status_code, 200)

    def test_access_delivery_points_list__with_unauthenticated_user__expect_redirect(self):
        response = self.client.get(reverse('routes:delivery_points_list'))
        self.assertEqual(response.status_code, 302)

    def test_acces_delivery_points_list__with_authenticated_user__expect_passes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('routes:delivery_points_list'))
        self.assertEqual(response.status_code, 200)


class PhotoURLValidateTests(TestCase):
    def setUp(self):
        self.validator = PhotoURLValidate('URL must point to a valid image file (.jpg, .jpeg, .png, .gif, .webp)')

    def test_empty_value_passes(self):
        self.validator('')

    def test_valid_jpg__expect_url_passes(self):
        self.validator('https://myimage.com/image.jpg')

    def test_valid_png__expect_url_passes(self):
        self.validator('https://myimage.com/image.png')

    def test_valid_webp_url__expect_passes(self):
        self.validator('https://myimage.com/image.webp')

    def test_invalid_extension__expect_error_raises(self):
        with self.assertRaises(ValidationError):
            self.validator('https://myimage.com/image.heic')

    def test_invalid_extension__expect_error_raises_and_shows_correct_message(self):
        with self.assertRaises(ValidationError) as ve:
            self.validator('https://myimage.com/image.heic')
        self.assertIn('URL must point to a valid image file (.jpg, .jpeg, .png, .gif, .webp)', str(ve.exception))

