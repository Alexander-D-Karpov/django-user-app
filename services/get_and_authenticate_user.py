from django.contrib.auth import authenticate

from common.error import ValidatorException


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise ValidatorException("User does not exist", "NoUser")
    return user
