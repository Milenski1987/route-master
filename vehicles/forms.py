from typing import Optional

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from common.forms import SearchForm
from common.mixins import ReadOnlyFieldsMixin
from vehicles.models import Vehicle


class VehicleSearchAndSortForm(SearchForm):
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('make', 'Make (A-Z)'),
            ('-make', 'Make (Z-A)'),
            ('capacity_kg', 'Capacity in kg (Low-High)'),
            ('-capacity_kg', 'Capacity in kg (High-Low)'),
        ],
        widget=forms.Select(
            {'class': 'form-select rounded-4'}
        )
    )


class BaseVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'registration_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Vehicle registration number...'
                }
            ),
            'make': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Vehicle make name...'
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Vehicle model...'
                }
            ),
            'photo': forms.URLInput(
                attrs={
                    'placeholder': 'Upload Vehicle photo...'
                }
            ),
            'vehicle_type':forms.Select(
                attrs={
                    'placeholder': 'Choose Vehicle type'
                }
            ),
            'capacity_kg': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter Vehicle capacity in kg...'
                }
            ),
            'manufacture_date': forms.DateInput(
                attrs={
                    'plaeholder': 'Enter Vehicle manufacture date...',
                    'type': 'date'
                }
            )
        }

        help_texts={
            'registration_number': 'Between 6 to 8 uppercase alphanumeric characters',
            'capacity_kg': 'Only positive integer numbers',
        }

        labels = {
            'capacity_kg': 'Capacity in kg'
        }

        error_messages = {
            'registration_number':{
                'required': 'Please enter Vehicle registration number!'
            },
            'make': {
                'required': 'Please enter Vehicle make name!'
            },
            'vehicle_type':{
                'required': 'Please choose Vehicle type from menu'
            },
            'capacity_kg':{
                'required': 'Please enter Vehicle capacity in kg',
                'invalid': 'Please enter valid capacity in kg'
            },
            'manufacture_date': {
                'required': 'Please choose manufacturare date'
            }
        }


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_manufacture_date(self)-> Optional[str]:
        date = self.cleaned_data.get('manufacture_date')
        if date > now().date():
            raise ValidationError("Manufacture date can't in the future")
        return date


    def save(self, commit = True):
        instance = super().save(commit=False)
        instance.make = instance.make.capitalize()

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class VehicleDeleteForm(ReadOnlyFieldsMixin, BaseVehicleForm):
    class Meta(BaseVehicleForm.Meta):
        widgets = {}
        help_texts = {}


class VehicleAddForm(BaseVehicleForm):
    ...


class VehicleEditForm(BaseVehicleForm):
    ...