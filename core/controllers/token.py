from ninja_extra import (
    ControllerBase,
    api_controller,
    route,
)
from typing import Optional
from core.models import Token, User  # Replace with actual models
from core.models.schemas import (
    RefreshTokenSchema,
    PatchTokenUpdate,
)
from core.exceptions import Error
from core.payload.auth import auth_user
from .. import coreLogger


@api_controller("/token", tags=["tokens"])
class TokenController(ControllerBase):
    @route.get("/list-tokens", response={200: RefreshTokenSchema, 404: Error})
    def list_tokens(self, username: str, password: str):
        """
        Endpoint to list tokens for a user, including the parent token and its children.
        """
        user = auth_user(username=username, password=password, request=self.context.request)
        if user:
            self.context.response.headers["X-User-Authed"] = "TRUE"
            user_profile = user.profile
            tokens_data = user_profile.get_primary_refresh()
            if not tokens_data:
                return 404, {"message": "No active parent token found for the user."}

            return tokens_data
        else:
            self.context.response.headers["X-User-Authed"] = "FALSE"
            return 404, {"message": "User not found."}

    @route.put("/update-token", response={200: RefreshTokenSchema, 404: Error})
    def update_token(self, payload: PatchTokenUpdate):
        """
        updates a refresh token and issues with new token.
        """
        refresh_token = payload.refresh_Token
        try:
            # token = Token.objects.filter()
            token = Token.refresh_primary_token(token=refresh_token)

            return token

            # raise HttpError(400, "Token rotation is not enabled.")
        except AttributeError as e:
            coreLogger.error(f"exp , {str(e)}")
            return 404, {"message": "this Token didnt obtained by user"}

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

    @route.post("/create-token", response={200: RefreshTokenSchema, 404: Error})
    def create_token(self, username: str, password):
        """
        creating token with username and password as login
        """
        user_Token = auth_user(
            username=username, password=password, request=self.context.request, get_token=True
        )
        if user_Token:
            return user_Token
        else:
            self.context.response.headers["X-User-Authed"] = "FALSE"
            return 404, {"message": "User not found."}
