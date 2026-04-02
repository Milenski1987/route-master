from rest_framework import serializers
from accounts.models import RouteMasterUser


class AdminDashboardSerializer(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField()

    class Meta:
        model = RouteMasterUser
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'user_groups']

    def get_user_groups(self, obj):
        return list(obj.groups.values_list('name', flat=True))