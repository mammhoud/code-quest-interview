from datetime import datetime
from typing import List, Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from ninja_extra import status
from ninja_extra.exceptions import APIException
from ninja_schema import ModelSchema, Schema, model_validator
from pydantic import field_validator


UserModel = get_user_model()


class GroupSchema(ModelSchema):
    """Schema for Django's Group model."""

    class Config:
        model = Group
        include = ("name",)


class CreateUserSchema(ModelSchema):
    """Schema to create a new user."""

    class Config:
        model = UserModel
        include = (
            "email",
            "username",
            "is_staff",
            "is_superuser",
            "password",
        )

    @model_validator("username")
    def unique_username(cls, value_data):
        """Validator to ensure the username is unique."""
        if UserModel.objects.filter(username__icontains=value_data).exists():  # todo change this with exact
            raise APIException(
                "Username already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return value_data

    @model_validator("email")
    def unique_email(cls, value_data):
        """Validator to ensure the email is unique."""
        if UserModel.objects.filter(email__icontains=value_data).exists():  # todo change this with exact
            raise APIException("Email already exists", status_code=status.HTTP_400_BAD_REQUEST)
        return value_data

    def create(self) -> Type[AbstractUser]:
        """Create a new user instance."""
        return UserModel.objects.create_user(**self.dict())


class CreateUserOutSchema(CreateUserSchema):
    """Schema to output user creation details including the token."""

    token: str

    class Config:
        model = UserModel
        exclude = ("password",)


class UserSchema(ModelSchema):
    """Schema to retrieve user details along with groups."""

    groups: List[GroupSchema]

    class Config:
        model = UserModel
        include = ["email", "username", "id", "is_active"]


class EnableDisableUserSchema(Schema):
    """Schema to enable or disable a user."""

    user_id: str
    _user: Optional[Type[AbstractUser]] = None

    @field_validator("user_id")
    def validate_user_id(cls, value):
        """Validator to ensure the user ID is valid."""
        user = UserModel.objects.filter(id=value).first()
        if user:
            cls._user = user
            return value
        raise ValueError("Invalid User ID")

    def update(self):
        """Toggle the active state of the user."""
        self._user.is_active = not self._user.is_active
        self._user.save()
        return self._user

    def delete(self):
        """Delete the user."""
        user_id = self._user.pk
        self._user.delete()
        return user_id


class EnableDisableUserOutSchema(Schema):
    """Schema for outputting the result of enabling or disabling a user."""

    message: str
