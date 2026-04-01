from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from accounts.choices import UIThemeChoices
from accounts.managers import RouteMasterUserManager
from accounts.validators import UserEmailValidator


class RouteMasterUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    employee_id = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6)
        ],
        unique=True
    )

    first_name = models.CharField(
        max_length= 50,
    )

    last_name = models.CharField(
        max_length= 50,
    )

    email = models.EmailField(
        unique=True,
        validators=[
            UserEmailValidator(
                'routemaster.com',
                "Please use your company email (e.g., example@routemaster.com)"
            )
        ],
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    objects = RouteMasterUserManager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} - Employee ID: {self.employee_id}'


class RouteMasterUserSettings(models.Model):
    user = models.OneToOneField(
        RouteMasterUser,
        on_delete=models.CASCADE,
        related_name='settings'
    )

    theme = models.CharField(
        max_length=15,
        choices=UIThemeChoices.choices,
        default=UIThemeChoices.LIGHT
    )
