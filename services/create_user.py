from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from common.error import ValidatorException
from user.models import Person
from user.services.validate_password import validate_password


def create_user(
    username: str,
    email: str,
    password: str,
    first_name="",
    last_name="",
    **extra_fields
) -> Person:
    """Create User instance"""
    try:
        validate_email(email)
    except ValidationError:
        raise ValidatorException("Provided email is not correct", "IncEMail")

    if len(password) < 8:
        raise ValidatorException("Provided passwords are different", "ShortPas")

    validate_password(password)

    if (
        Person.objects.filter(username=username).exists()
        or Person.objects.filter(email=email).exists()
    ):
        raise ValidatorException("User already exists", "NoUser")
    else:
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        return user
