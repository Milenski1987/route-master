from datetime import timedelta
from math import ceil
from django import template
from routes.models import Assignment


register = template.Library()

@register.simple_tag()
def calculate_eta(assignment: Assignment):
    average_speed_by_vehicle = {
        'truck': 70,
        'van': 80,
        'car': 90
    }

    average_speed = average_speed_by_vehicle[assignment.vehicle.vehicle_type.lower()]
    route_distance = assignment.route.distance_km

    total_time = route_distance/average_speed

    total_hours = int(total_time) + 8
    total_minutes = ceil((total_time - int(total_time)) * 60)

    delivery_date = assignment.assignment_start

    if total_hours > 24:
        delivery_date += timedelta(days=total_hours // 24)
        total_hours -= total_hours // 24

    return f'{delivery_date.strftime("%d.%m.%Y")}, {total_hours:02d}:{total_minutes:02d}'