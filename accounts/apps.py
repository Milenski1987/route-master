from django.apps import AppConfig


def create_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    manager_codenames = [
        'add_route', 'change_route', 'delete_route', 'view_route',
        'add_deliverypoint', 'change_deliverypoint', 'delete_deliverypoint', 'view_deliverypoint',
        'add_assignment', 'change_assignment', 'delete_assignment', 'view_assignment',
        'add_driver', 'change_driver', 'delete_driver', 'view_driver',
        'add_vehicle', 'change_vehicle', 'delete_vehicle', 'view_vehicle',
        'add_specialization', 'change_specialization', 'delete_specialization', 'view_specialization'
    ]

    driver_codenames = [
        'view_route',
        'view_deliverypoint',
        'view_assignment',
        'view_driver',
        'view_vehicle',
        'view_specialization'
    ]

    manager_group, _ = Group.objects.get_or_create(name='Managers')
    driver_group, _ = Group.objects.get_or_create(name='Drivers')

    manager_perms = Permission.objects.filter(codename__in=manager_codenames)
    driver_perms = Permission.objects.filter(codename__in=driver_codenames)

    manager_group.permissions.set(manager_perms)
    driver_group.permissions.set(driver_perms)


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_groups_and_permissions, sender=self)

