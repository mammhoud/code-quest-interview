from ninja_extra import (
    ControllerBase,
    api_controller,
    route,
)
from typing import Optional
from core.models import Token, User  # Replace with actual models
from core.models.schemas import RefreshTokenSchema, PatchTokenUpdate, TokenListResponse, AccessTokenSchema
from core.exceptions import Error
from core.payload.auth import auth_user
from .. import coreLogger
from core.authentications.ninja import GlobalAuth


@api_controller("/token", tags=["tokens"])
class TokenController(ControllerBase):
    @route.get("/get-refresh", response={200: RefreshTokenSchema, 404: Error})
    def get_refresh_token(self, username: str, password: str):
        """
        Endpoint to get token for a user, including the parent token and its children.
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

    @route.post("/update-token", response={200: RefreshTokenSchema, 404: Error})
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

    @route.delete("/revoke-token", response={200: str, 404: Error})
    def revoke_token(self, refresh_token: str):
        """
        Revokes a refresh token by blacklisting it.
        """
        # try:
        token = Token.objects.filter(token=refresh_token).first()
        if token:
            token.revoke()
            # refresh = RefreshToken(refresh_token)
            # refresh.blacklist()
            return 200, "Token successfully revoked."
        else:
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

    @route.get("/get-tokens", response={200: TokenListResponse, 404: Error}, auth=GlobalAuth())
    def get_access_tokens(self, request):
        tokens = None
        try:
            authed_token = self.context.request.token
            authed_user = self.context.request.user
            tokens = authed_token.get_all_access_tokens(authed_user)
        except ValueError as e:
            coreLogger.error(f"exp , {str(e)}")
            return 404, {"message": "token should be a refresh token"}
        if not tokens:
            return 404, {"message": "token should be a refresh token"}

        return 200, tokens

    @route.put("/access-token", response={200: AccessTokenSchema, 404: Error}, auth=GlobalAuth())
    def create_access_token(self, request):
        token = None
        try:
            authed_profile = self.context.request.profile
            token = authed_profile.create_access_token()
        except ValueError as e:
            coreLogger.error(f"exp , {str(e)}")
            return 404, {"message": "token should be a refresh token"}
        if not token:
            return 404, {"message": "token should be a refresh token"}

        return 200, token


