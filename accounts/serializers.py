from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import RouteMasterUser


class AdminDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteMasterUser
        fields = ['employee_id', 'first_name', 'last_name', 'email']