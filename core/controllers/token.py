from ninja_extra import (
    ControllerBase,
    api_controller,
    route,
)
from typing import List, Optional
from django.utils.translation import gettext_lazy as _
from core import exceptions
from core.models import Token, User  # Replace with actual models
from core.models.schemas import RefreshTokenSchema, PatchTokenUpdate, TokenListResponse, AccessTokenSchema
from core.exceptions import Error
from core.payload.auth import auth_user
from .. import coreLogger as logger
from core.authentications.ninja import GlobalAuth
from core.models.schemas import ValidateToken


@api_controller("/token", tags=["tokens"])
class TokenController(ControllerBase):
    @route.get("/get-refresh", response={200: RefreshTokenSchema, 404: Error})
    def get_refresh_token(self, username: str, password: str):
        """
        Retrieve the primary refresh token for a user, if authentication succeeds.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            RefreshTokenSchema: The primary refresh token object if found.
        """
        user = auth_user(username=username, password=password, request=self.context.request)
        if user:
            self.context.response.headers["X-User-Authed"] = "TRUE"
            user_profile = user.profile
            tokens_data = user_profile.get_primary_refresh()
            if not tokens_data:
                return 404, {"message": _("No active parent token found for the user.")}
            return tokens_data
        else:
            self.context.response.headers["X-User-Authed"] = "FALSE"
            return 404, {"message": _("User not found.")}

    @route.post("/update-token", response={200: RefreshTokenSchema, 404: Error})
    def update_token(self, payload: PatchTokenUpdate):
        """
        Update a refresh token by rotating it and issuing a new one.

        Args:
            payload (PatchTokenUpdate): Contains the current refresh token to be updated.

        Returns:
            RefreshTokenSchema: The newly issued refresh token object.
        """
        refresh_token = payload.refresh_Token
        try:
            token = Token.refresh_primary_token(token=refresh_token)
            return token
        except AttributeError as e:
            coreLogger.error(f"Token update failed: {e}")
            return 404, {"message": _("This token was not obtained by the user.")}
        except Exception as e:
            coreLogger.warning(f"Unexpected error in update_token: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.delete("/revoke-token", response={200: str, 404: Error})
    def revoke_token(self, refresh_token: str):
        """
        Revoke a refresh token, making it invalid for further use.

        Args:
            refresh_token (str): The token string to revoke.

        Returns:
            str: Success message or error.
        """
        try:
            token = Token.objects.filter(token=refresh_token).first()
            if token:
                token.revoke()
                return 200, _("Token successfully revoked.")
            else:
                return 404, {"message": _("This token was not obtained by the user.")}
        except Exception as e:
            coreLogger.warning(f"Unexpected error in revoke_token: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.post("/create-token", response={200: RefreshTokenSchema, 404: Error})
    def create_token(self, username: str, password):
        """
        Authenticate a user and return a newly created token pair.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            RefreshTokenSchema: Token details upon successful authentication.
        """
        try:
            user_token = auth_user(
                username=username, password=password, request=self.context.request, get_token=True
            )
            if user_token:
                return user_token
            else:
                self.context.response.headers["X-User-Authed"] = "FALSE"
                return 404, {"message": _("User not found.")}
        except Exception as e:
            coreLogger.warning(f"Unexpected error in create_token: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.get("/get-tokens", response={200: TokenListResponse, 404: Error}, auth=GlobalAuth())
    def get_access_tokens(self, request):
        """
        Retrieve all access tokens generated from a valid refresh token.

        Requires authentication.

        Returns:
            TokenListResponse: A list of access tokens grouped under a refresh token.
        """
        try:
            authed_token = self.context.request.token
            authed_user = self.context.request.user
            tokens = authed_token.get_all_access_tokens(authed_user)
            if not tokens:
                raise ValueError(_("Token must be a valid refresh token."))
            return 200, tokens
        except ValueError as e:
            coreLogger.error(f"Invalid token type: {e}")
            return 404, {"message": str(e)}
        except Exception as e:
            coreLogger.warning(f"Unexpected error in get_access_tokens: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.put("/access-token", response={200: AccessTokenSchema, 404: Error}, auth=GlobalAuth())
    def create_access_token(self, request):
        """
        Create a new access token using the authenticated refresh token.

        Requires authentication.

        Returns:
            AccessTokenSchema: Newly issued access token object.
        """
        try:
            authed_profile = self.context.request.profile
            token = authed_profile.create_access_token()
            if not token:
                raise ValueError(_("Token must be a valid refresh token."))
            return 200, token
        except ValueError as e:
            coreLogger.error(f"Invalid refresh token: {e}")
            return 404, {"message": str(e)}
        except Exception as e:
            coreLogger.warning(f"Unexpected error in create_access_token: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.get("/access-tokens", response={200: List[AccessTokenSchema], 404: Error, 500: Error})
    def list_access_tokens(self, request):
        """
        List all active access tokens for the currently authenticated user.

        Returns:
            List[AccessTokenSchema]: A list of active access token objects.
        """
        try:
            authed_profile = self.context.request.profile
            primary = authed_profile.get_primary_refresh()
            if not primary:
                return 404, {"message": _("No valid primary refresh token found.")}
            access_tokens = Token.get_active_tokens(request.user).filter(
                token_type=Token.ACCESS, parent=primary
            )
            return access_tokens
        except Exception as e:
            coreLogger.warning(f"Unexpected error in list_access_tokens: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.get("/token-tree", response={200: TokenListResponse, 404: Error, 500: Error})
    def get_token_tree(self, request):
        """
        Return a tree representation of a user's tokens including the refresh token
        and its linked access tokens.

        Returns:
            TokenListResponse: Parent refresh token and its associated access tokens.
        """
        try:
            authed_profile = self.context.request.profile
            primary = authed_profile.get_primary_refresh()
            if not primary:
                return 404, {"message": _("No valid primary refresh token found.")}

            access_tokens = Token.get_active_tokens(request.user).filter(
                token_type=Token.ACCESS, parent=primary
            )

            return {"parent": primary, "children": list(access_tokens)}

        except Exception as e:
            coreLogger.warning(f"Unexpected error in get_token_tree: {e}")
            return 500, {"message": _("An unexpected error occurred.")}

    @route.post("/rotate-token", response={200: ValidateToken, 400: Error, 500: Error})
    def rotate_token(self, payload: ValidateToken):
        """
        Rotate the provided refresh token and issue new tokens.

        Args:
        ----------
        payload (ValidateToken): Contains the refresh token to be rotated.

        Returns:
        ----------
        200:
            Returns the validated tokens including a new access token and optionally a new refresh token.
        400:
            Returns an error message when the provided token is invalid.
        500:
            Returns an error message for unexpected server errors.

        Description:
        ----------
        - Accepts a refresh token to rotate via the request payload.
        - Validates the token using `ValidateToken` schema.
        - Upon successful validation, returns updated token data.
        - Properly handles and logs validation and unexpected errors.
        """
        try:
            validated = payload.dict()
            return 200, validated
        except exceptions.ValidationError as e:
            coreLogger.error(f"Validation error rotating token: {e}")
            return 400, {"message": "Invalid token provided."}
        except Exception as e:
            coreLogger.warning(f"Unexpected error rotating token: {e}")
            return 500, {"message": "An unexpected error occurred."}
