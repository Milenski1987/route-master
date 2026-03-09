from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import RouteMasterUserSettings

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        RouteMasterUserSettings.objects.create(user=instance)