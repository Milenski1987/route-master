from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsViewsTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.valid_user = self.user_model.objects.create_user(
            employee_id= "100000",
            first_name= "Milen",
            last_name= "Nikolov",
            email= "m.nikolov@routemaster.com",
            password= "P0werPass"
        )

    def test_register__with_valid_data__expect_create_user_success(self):
        response = self.client.post(
            reverse('accounts:register'),
            data={
                "employee_id": "200000",
                "first_name": "Milena",
                "last_name": "Nikolova",
                "email": "m.nikolova@routemaster.com",
                "password1": "P0werR0ute",
                "password2": "P0werR0ute"
            }
        )

        self.assertTrue(self.user_model.objects.filter(employee_id='200000').exists())


    def test_register__with_invalid_data__expect_create_user_fail(self):
        response = self.client.post(
            reverse('accounts:register'),
            data={
                "employee_id": "200000",
                "first_name": "Milena",
                "last_name": "Nikolova",
                "email": "m.nikolova@routemaster.bg",
                "password1": "P0werR0ute",
                "password2": "P0werR0ute"
            }
        )

        self.assertFalse(self.user_model.objects.filter(employee_id='200000').exists())


    def test_login__with_valid_credentials__expect_redirect(self):
        response = self.client.post(
            reverse('accounts:login'),
            data= {
            'username': '100000',
            'password': 'P0werPass',
        })
        self.assertEqual(response.status_code, 302)


    def test_login__with_invalid_credentials__expect_no_redirect(self):
        response = self.client.post(
            reverse('accounts:login'),
            data= {
            'username': '100000',
            'password': 'PowerPass',
        })
        self.assertEqual(response.status_code, 200)


    def test_logout__expect_redirect(self):
        self.client.force_login(self.valid_user)
        response = self.client.post(
            reverse('accounts:logout')
        )

        self.assertEqual(response.status_code, 302)

