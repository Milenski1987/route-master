from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UserEmailValidator:
    def __init__(self, domain: str, wrong_domain_message: str) -> None:
        self.domain = domain
        self.wrong_domain_message = wrong_domain_message

    def __call__(self, value: str) -> None:
        domain = value.split('@')[1]
        if domain != self.domain:
            raise ValidationError(self.wrong_domain_message)

