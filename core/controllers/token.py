from datetime import datetime

from django.utils.timezone import now
from ninja_extra import (
    ControllerBase,
    api_controller,
    route,
)
from ninja_jwt.exceptions import ValidationError
from ninja_jwt.settings import api_settings

# from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken

import logging

# from core import loggerRequest as logger  # type: ignore

# from ninja_jwt.token_blacklist import OutstandingToken
logger = logging.getLogger(__name__)
from core.models import Token, User  # Replace with actual models
from core.models.schemas import (
    AccessTokenSchema,
    RefreshTokenSchema,
    TokenListResponse,
    TokenSchema,
    UserSchema,
)
from core.exceptions import Error


@api_controller("/token", tags=["tokens"])
class TokenController(ControllerBase):
    @route.get("/list-tokens", response={200: TokenListResponse, 404: Error})
    def list_tokens(self, username: str):
        """
        Endpoint to list tokens for a user, including the parent token and its children.
        """
        try:
            # Retrieve the user
            user = User.objects.get(username=username, is_active=True)

            print(f"User: {user.username}, ID: {user.id}")
            user_profile = user.profile

            # Fetch the parent token (assuming one active refresh token per user)
            tokens_data = user_profile.get_primary_refresh()
            print(f"Tokens Data: {tokens_data}")
            if not tokens_data:
                return 404, "No active parent token found for the user."

            return tokens_data

        except User.DoesNotExist:
            return 404, "User not found."

    @route.post("/update-token", response={200: TokenSchema, 404: Error})
    def update_token(self, refresh_token: str):
        """
        updates a refresh token and issues with new token.
        """
        try:
            # token = Token.objects.filter()
            token = Token.refresh_primary_token(token=refresh_token)

            return {
                "user": None,
                "token": str(token.token),
                "exp": token.exp,
                "is_revoked": False,
            }

            # raise HttpError(400, "Token rotation is not enabled.")
        except AttributeError as e:
            print(f"exp , {str(e)}")
            return 404, {"message": "this Token didnt obtained by user"}
        # except Exception as e:
        #     loggerAPI.error(500, str(e.__str__))

    @route.post("/revoke-token", response={200: str})
    def revoke_token(self, refresh_token: str):
        """
        Revokes a refresh token by blacklisting it.
        """
        try:
            token = Token.objects.filter(token=refresh_token).first()
            if token:
                token.revoke()
            # refresh = RefreshToken(refresh_token)
            # refresh.blacklist()
            return "Token successfully revoked."
        except AttributeError:
            return 404, {"message": "this Token didnt obtained by user"}
