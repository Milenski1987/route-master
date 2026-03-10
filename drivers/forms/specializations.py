from django import forms
from common.mixins import ReadOnlyFieldsMixin
from drivers.models import Specialization


class BaseSpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter specialization name...'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter specialization description...'
                }
            )
        }

        help_texts={
            'name': 'Name or Title of specializaiton',
        }


        error_messages = {
            'name':{
                'required': 'Please enter Driver name!'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SpecializationDeleteForm(ReadOnlyFieldsMixin, BaseSpecializationForm):
    class Meta(BaseSpecializationForm.Meta):
        widgets = {}
        help_texts = {}


class SpecializationAddForm(BaseSpecializationForm):
    ...


class SpecializationEditForm(BaseSpecializationForm):
    ...