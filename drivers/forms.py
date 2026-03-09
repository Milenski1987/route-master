from django import forms
from common.forms import SearchForm
from common.mixins import ReadOnlyFieldsMixin
from drivers.models import Driver


class DriverSearchAndSortForm(SearchForm):
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('full_name', 'Name (A-Z)'),
            ('-full_name', 'Name (Z-A)'),
            ('years_of_experience', 'Experience (Low-High)'),
            ('-years_of_experience', 'Experience (High-Low)'),
        ],
        widget=forms.Select(
            {'class': 'form-select rounded-4'}
        )
    )


class BaseDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Driver full name...'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'Enter Driver birth date...'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter phone number...'
                }
            ),
            'photo': forms.URLInput(
                attrs={
                    'placeholder': 'Photo upload...'
                }
            ),
            'driving_license_number':forms.TextInput(
                attrs={
                    'placeholder': 'Driving license number...'
                }
            ),
            'years_of_experience': forms.NumberInput(
                attrs={
                    'placeholder': 'Years of experience'
                }
            )
        }

        help_texts={
            'years_of_experience': 'Only integer numbers',
            'driving_license_number': 'Enter 10 uppercase alphanumeric characters'
        }

        labels = {
            'distance_km': 'Distance in km'
        }

        error_messages = {
            'full_name':{
                'required': 'Please enter Driver name!'
            },
            'phone_number': {
                'required': 'Please enter valid phone number!'
            },
            'driving_license_number':{
                'required': 'Please enter Driving license number'
            },
            'years_of_experience':{
                'required': 'Please enter years of experience',
                'invalid': 'Please enter valid positive number'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class DriverDeleteForm(ReadOnlyFieldsMixin, BaseDriverForm):
    class Meta(BaseDriverForm.Meta):
        widgets = {}
        help_texts = {}


class DriverAddForm(BaseDriverForm):
    ...


class DriverEditForm(BaseDriverForm):
    ...