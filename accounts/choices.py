from django.db import models


class UIThemeChoices(models.TextChoices):
    DARK = 'Dark', 'Dark'
    LIGHT = 'Light', 'Light'