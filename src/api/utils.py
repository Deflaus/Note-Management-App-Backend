from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


def check_password_complexity(password: str) -> None:
    error_messages = []

    try:
        password_validation.validate_password(password=password)
    except DjangoValidationError as e:
        for password_error in e.error_list:
            error_messages.extend(password_error.messages)

    if error_messages:
        raise ValidationError(error_messages)
