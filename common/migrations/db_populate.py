from django.contrib.auth.hashers import make_password
from django.db import migrations
import random
import string
from datetime import date, timedelta


FIRST_NAMES = [
    "Ivan", "Georgi", "Petar", "Nikolay", "Dimitar", "Stoyan", "Vasil", "Hristo", "Atanas", "Krasimir",
    "Milen", "Bozhidar", "Mario", "Alexandar", "Teodor", "Martin", "Ivailo", "Angel", "Stanislav"
]

LAST_NAMES = [
    "Ivanov", "Petrov", "Georgiev", "Dimitrov", "Nikolov", "Hristov", "Stoyanov", "Vasilev", "Atanasov",
    "Alexandrov", "Todorov", "Zahariev", "Iliev", "Markov", "Spasov", "Angelov", "Tashev", "Petkov"
]

CITIES = [
    "Sofia", "Plovdiv", "Varna", "Burgas", "Ruse", "Blagoevgrad", "Shumen", "Pleven", "Vratsa", "Silistra",
    "Sandanski", "Montanta", "Vidin", "Stara Zagora", "Haskovo", "Yambol", "Veliko Tarnovo"
]

REGION_CODES = [
    "C", "CA", "CB", "PB", "B", "BT", "EH", "A", "H", "BP", "CT", "P", "CC", "E", "M", "BH", "X", "Y"
]

VEHICLE_TYPES = ["Truck", "Van", "Car"]

VEHICLE_MAKE = ["Mercedes", "Volvo", "MAN", "Scania", "DAF", "Ford"]

def generate_plate(existing):
    while True:
        region = random.choice(REGION_CODES)
        numbers = str(random.randint(1000, 9999))
        letters = random.choice(REGION_CODES)
        plate = f"{region}{numbers}{letters}"
        if plate not in existing:
            existing.add(plate)
            return plate

def generate_license(existing):
    while True:
        license_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if license_number not in existing:
            existing.add(license_number)
            return license_number

def generate_phone(existing):
    while True:
        phone = f"08{random.randint(70000000, 99999999)}"
        if phone not in existing:
            existing.add(phone)
            return phone

def generate_data(apps, schema_editor):
    Driver = apps.get_model("drivers", "Driver")
    Specialization = apps.get_model("drivers", "Specialization")
    Vehicle = apps.get_model("vehicles", "Vehicle")
    DeliveryPoint = apps.get_model("routes", "DeliveryPoint")
    Route = apps.get_model("routes", "Route")
    Assignment = apps.get_model("routes", "Assignment")
    User = apps.get_model("accounts", "RouteMasterUser")
    Group = apps.get_model('auth', 'Group')
    UserSettings = apps.get_model('accounts', 'RouteMasterUserSettings')

    manager_group, _ = Group.objects.get_or_create(name='Managers')
    driver_group, _ = Group.objects.get_or_create(name='Drivers')

    manager_user = User.objects.create(
        employee_id='000001',
        first_name='Manager',
        last_name='One',
        email='manager@routemaster.com',
        is_staff=True
    )
    manager_user.password = make_password('manager123')
    manager_user.save()
    manager_user.groups.add(manager_group)

    driver_user = User.objects.create(
        employee_id='000002',
        first_name='Driver',
        last_name='One',
        email='driver@routemaster.com',
        is_staff=False
    )
    driver_user.password = make_password('driver123')
    driver_user.save()
    driver_user.groups.add(driver_group)

    UserSettings.objects.create(user=manager_user)
    UserSettings.objects.create(user=driver_user)

    used_phones = set()
    used_licenses = set()
    drivers = []

    skills = []
    for i in range(20):
        skill = Specialization.objects.create(
            name=f"Skill {i}",
            description='Driver skill'
        )
        skills.append(skill)
    for _ in range(30):
        birth_year = random.randint(1965, 2007)
        driver = Driver.objects.create(
            full_name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            date_of_birth=date(birth_year, random.randint(1, 12), random.randint(1, 28)),
            phone_number=generate_phone(used_phones),
            driving_license_number=generate_license(used_licenses),
            years_of_experience=random.randint(0, date.today().year - birth_year - 18),
            photo=f"https://randomuser.me/api/portraits/men/{random.randint(0, 99)}.jpg"
        )
        driver.specializations.add(*random.sample(skills, k=random.randint(0, 5)))
        drivers.append(driver)

    used_plates = set()
    vehicles = []
    for _ in range(30):
        vehicle = Vehicle.objects.create(
            registration_number=generate_plate(used_plates),
            make=random.choice(VEHICLE_MAKE),
            model=''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
            vehicle_type=random.choice(VEHICLE_TYPES),
            capacity_kg=random.randint(500, 25000),
            manufacture_date=date(random.randint(2010, 2025), random.randint(1, 12), random.randint(1, 28)),
        )
        vehicles.append(vehicle)

    points = []
    for i in range(60):
        point = DeliveryPoint.objects.create(
            name=f"Warehouse {i}",
            address=f"Street {i}",
            city=random.choice(CITIES),
            description="Logistics hub"
        )
        points.append(point)

    routes = []
    for _ in range(80):
        start = random.choice(CITIES)
        end = random.choice([c for c in CITIES if c != start])
        route = Route.objects.create(
            name=f"{start} - {end}",
            start_location=start,
            end_location=end,
            distance_km=random.randint(50, 1000)
        )
        route.points_for_delivery.add(*random.sample(points, k=random.randint(0, 5)))
        routes.append(route)

    today = date.today()
    used_driver_date = set()
    used_vehicle_date = set()
    assignments = []

    def create_assignment(target_date):
        while True:
            driver = random.choice(drivers)
            vehicle = random.choice(vehicles)
            if (driver.id, target_date) in used_driver_date:
                continue
            if (vehicle.id, target_date) in used_vehicle_date:
                continue
            used_driver_date.add((driver.id, target_date))
            used_vehicle_date.add((vehicle.id, target_date))
            return Assignment(
                route=random.choice(routes),
                driver=driver,
                vehicle=vehicle,
                assignment_start=target_date,
                notes=random.choice(["Standard delivery","Fragile goods","Cold transport","Express delivery"])
            )

    for _ in range(52):
        past_date = today - timedelta(days=random.randint(1, 90))
        assignments.append(create_assignment(past_date))

    for _ in range(70):
        future_date = today + timedelta(days=random.randint(1, 90))
        assignments.append(create_assignment(future_date))

    Assignment.objects.bulk_create(assignments)

def reverse_func(apps, schema_editor):
    Driver = apps.get_model("drivers", "Driver")
    Vehicle = apps.get_model("vehicles", "Vehicle")
    DeliveryPoint = apps.get_model("routes", "DeliveryPoint")
    Route = apps.get_model("routes", "Route")
    Assignment = apps.get_model("routes", "Assignment")
    User = apps.get_model("accounts", "RouteMasterUser")
    Group = apps.get_model('auth', 'Group')

    Assignment.objects.all().delete()
    Route.objects.all().delete()
    DeliveryPoint.objects.all().delete()
    Vehicle.objects.all().delete()
    Driver.objects.all().delete()
    User.objects.filter(employee_id__in=['000001','000002']).delete()
    Group.objects.filter(name__in=['Managers','Drivers']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('drivers', '0001_initial'),
        ('vehicles', '0001_initial'),
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_data, reverse_func),
    ]