from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ninja import Schema

from typing import Any, Optional, List
from ninja import Schema
from pydantic import model_validator, model_validator
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.utils import token_error
from ninja_jwt import exceptions
from ninja_jwt.settings import api_settings
from datetime import datetime
from ninja.schema import DjangoGetter
from .user import UserSchema


# Schema for token details
class TokenSchema(Schema):
    user: Optional[UserSchema]
    token: str
    exp: datetime
    is_revoked: bool


# # Validation schema for incoming token payload
# class ValidateToken(Schema):
#     refresh_token: Optional[TokenSchema] = None  # parent
#     access_tokens: Optional[List[TokenSchema]] = None  # children

#     @model_validator(mode="before")
#     @token_error
#     def validate_schema(cls, values: DjangoGetter) -> Any:
#         values = values._obj

#         if isinstance(values, dict):
#             if not values.get("parent"):
#                 raise exceptions.ValidationError({"refresh": "refresh token is required"})

#             refresh = RefreshToken(values["parent"])

#             data = {"access": str(refresh.access_token)}

#             if api_settings.ROTATE_REFRESH_TOKENS:
#                 if api_settings.BLACKLIST_AFTER_ROTATION:
#                     try:
#                         # Attempt to blacklist the given refresh token
#                         refresh.blacklist()
#                     except AttributeError:
#                         # If blacklist app not installed, `blacklist` method will
#                         # not be present
#                         pass

#                 refresh.set_jti()
#                 refresh.set_exp()
#                 refresh.set_iat()

#                 data["refresh"] = str(refresh)
#             values.update(data)
#         return values


class _TokenSchema(Schema):
    jti: str
    token: str
    type: str


class AccessTokenSchema(Schema):
    jti: UUID
    token_type: str
    exp: datetime
    token: Optional[str]
    usage: str


class RefreshTokenSchema(Schema):
    jti: UUID
    token_type: str
    exp: datetime
    token: Optional[str]
    usage: str


class TokenListResponse(Schema):
    parent: RefreshTokenSchema
    children: List[AccessTokenSchema]


class PatchTokenUpdate(Schema):
    refresh_Token: Optional[str] = None
    access_Token: Optional[str] = None
    
    username: Optional[str] = None
    password: Optional[str] = None
