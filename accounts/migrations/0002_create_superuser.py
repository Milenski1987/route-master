from django.db import migrations

def create_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if not User.objects.filter(employee_id='000000').exists():
        User.objects.create_superuser(
            employee_id='000000',
            first_name='Admin',
            last_name='Admin',
            email='admin@routemaster.com',
            password='admin123',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, migrations.RunPython.noop),
    ]