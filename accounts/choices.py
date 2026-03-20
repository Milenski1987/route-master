from django.db import models


class UIThemeChoices(models.TextChoices):
    DARK = 'dark', 'Dark'
    LIGHT = 'light', 'Light'