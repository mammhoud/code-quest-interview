from typing import Any
from uuid import UUID
from django.utils.timezone import datetime
from ninja import Schema
from pydantic import model_validator
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.utils import token_error
from ninja_jwt import exceptions
from ninja_jwt.settings import api_settings
from ninja.schema import DjangoGetter
from .user import UserSchema


class TokenSchema(Schema):
    """
    Represents a generic token structure including metadata and ownership.

    Attributes:
        user (Optional[UserSchema]): The user associated with the token.
        token (str): The token string.
        exp (datetime): The expiration datetime of the token.
        is_revoked (bool): Flag indicating if the token is revoked.
    """

    user: UserSchema | None
    token: str
    exp: datetime
    is_revoked: bool


class _TokenSchema(Schema):
    """
    Basic representation of a token with identifiers.

    Attributes:
        jti (str): The unique identifier for the token.
        token (str): The token string.
        type (str): The type of the token (e.g., access, refresh).
    """

    jti: str
    token: str
    type: str


class AccessTokenSchema(Schema):
    """
    Schema for representing an access token and its properties.

    Attributes:
        jti (UUID): Unique token identifier.
        token_type (str): Type of the token.
        exp (datetime): Expiration datetime.
        token (Optional[str]): The token string (optional).
        usage (str): Usage purpose or description.
    """

    jti: UUID
    token_type: str | None
    token: str | None
    exp: datetime | None
    usage: str


class RefreshTokenSchema(Schema):
    """
    Schema for representing a refresh token and its properties.

    Attributes:
        jti (UUID): Unique token identifier.
        token_type (str): Type of the token.
        exp (datetime): Expiration datetime.
        token (Optional[str]): The token string (optional).
        usage (str): Usage purpose or description.
    """

    jti: UUID
    token_type: str | None
    exp: datetime
    token: str | None
    usage: str


class TokenListResponse(Schema):
    """
    Schema for representing a hierarchical token structure.

    Attributes:
        parent (RefreshTokenSchema): The parent refresh token.
        children (list[AccessTokenSchema]): List of associated access tokens.
    """

    parent: RefreshTokenSchema
    childrens: list[AccessTokenSchema]


class PatchTokenUpdate(Schema):
    """
    Schema for updating token credentials or authentication.

    Attributes:
        refresh_Token (Optional[str]): The refresh token to be updated.
        access_Token (Optional[str]): An optional access token for context.
        username (Optional[str]): Username for authentication.
        password (Optional[str]): Password for authentication.
    """

    refresh_Token: str | None = None
    access_Token: str | None = None
    username: str | None = None
    password: str | None = None


class ValidateToken(Schema):
    """
    Validation schema for incoming token rotation payload.

    Fields:
    ----------
    refresh_token: Optional[str]
        The parent refresh token required to rotate tokens.

    access_tokens: Optional[list[str]]
        Optional list of child access tokens.

    Validation Process:
    ----------
    - Checks that the refresh token is present.
    - Instantiates a RefreshToken object from the provided refresh token.
    - Creates a new access token associated with the refresh token.
    - If ROTATE_REFRESH_TOKENS is enabled in settings:
        - Attempts to blacklist the old refresh token if BLACKLIST_AFTER_ROTATION is enabled.
        - Sets a new JTI, expiration, and issued-at timestamps on the refreshed token.
    - Updates the incoming payload with the new tokens.
    """

    refresh_token: str | None = None
    access_tokens: list[str] | None = None

    @model_validator(mode="before")
    @token_error
    def validate_schema(cls, values: DjangoGetter) -> Any:
        # Pre-process input payload before model instantiation
        values = values._obj

        if isinstance(values, dict):
            if not values.get("refresh_token"):
                raise exceptions.ValidationError({"refresh_token": "refresh token is required"})

            refresh = RefreshToken(values["refresh_token"])

            data = {"access": str(refresh.access_token)}

            if api_settings.ROTATE_REFRESH_TOKENS:
                if api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        # blacklist method not available if blacklist app not installed
                        pass

                refresh.set_jti()
                refresh.set_exp()
                refresh.set_iat()

                data["refresh"] = str(refresh)
            values.update(data)
        return values
