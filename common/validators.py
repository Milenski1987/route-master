from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhotoURLValidate:
    VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    def __init__(self, error_message):
        self.error_message = error_message

    def __call__(self, value: str) -> None:
        if value and value.split('.')[-1] not in self.VALID_EXTENSIONS:
            raise ValidationError(self.error_message)