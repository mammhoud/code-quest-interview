from django.contrib.auth import authenticate
from core.models.token import Token
from django.contrib.auth import get_user_model
from .. import coreLogger

User = get_user_model()


def auth_user(username: str, password: str, request=None, get_token=False):
    """
    Authenticate a user with the given username and password.
    """
    # Here you would typically check the username and password against your database
    # For demonstration, let's assume we have a function `authenticate_user` that does this
    user = None
    if request:
        user = authenticate(username=username, password=password, request=request)
    else:
        user = User.objects.filter(username=username, password=password, is_active=True)
    if not user:
        return False
    else:
        if get_token:
            return get_ProfileOrToken(user)
        return user


def get_ProfileOrToken(user: User = None, token: Token = None) -> str: # type: ignore
    """
    Get the token for the given user.
    """
    if not isinstance(user, User):
        coreLogger.error("method: get_ProfileOrToken; should take a user instance")
        return None

    