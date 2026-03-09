from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from accounts.models import RouteMasterUserSettings

UserModel = get_user_model()

class RouteMasterRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('employee_id', 'first_name', 'last_name', 'email')

        widgets = {
            'employee_id': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your 6 characters Employee ID'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name (e.g. John)'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name (e.g. Doe)'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Company email (e.g. example@routemaster.com)'
                }
            )
        }

        labels = {
            'employee_id': 'Employee ID',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }


        error_messages = {
            'employee_id':{
                'required': 'Please enter your Employee ID',
                'invalid': 'Employee ID must be exact 6 characters long'
            },
            'first_name':{
                'required': 'Please enter your first name'
            },
            'last_name': {
                'required': 'Please enter your last name'
            },
            'email':{
                'required': 'Please enter your company issued email address',
                'invalid': 'Please enter valid email address'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].widget.attrs['placeholder'] = 'Enter desired password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter desired password again'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = 'Password must be at lease 8 characters long'  # removes Django's default password hint list
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = 'Please enter your password again'


class RouteMasterLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['username'].label = 'Employee ID'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter you Employee ID here...'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password here...'

class UserThemeForm(forms.ModelForm):
    class Meta:
        model = RouteMasterUserSettings
        exclude = ['user']

class RouteMasterChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('employee_id', 'first_name', 'last_name', 'email')