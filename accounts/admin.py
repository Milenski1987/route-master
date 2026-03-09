from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from accounts.forms import RouteMasterRegisterForm, RouteMasterChangeForm


UserModel = get_user_model()

@admin.register(UserModel)
class RouteMasterUserAdmin(UserAdmin):
    model = UserModel
    add_form = RouteMasterRegisterForm
    form = RouteMasterChangeForm

    ordering = ('employee_id',)

    list_display = ('employee_id', 'first_name', 'last_name','email', 'is_staff')
    list_filter =  ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('employee_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
