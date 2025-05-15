from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer
from pprint import pprint
from core.models import Token
class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        # Assuming you have a method to validate the token
        token = Token.objects.filter(token=token).first()
        if token.is_valid():
            return token
        return None
