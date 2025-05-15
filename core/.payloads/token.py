# from secrets import token_hex

# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from ninja.errors import AuthenticationError  # type: ignore
# from ninja_jwt.tokens import RefreshToken, AccessToken  # type: ignore
# from ninja_jwt.settings import api_settings
# # from core.auth_app.models.schemas import TokenDataSchema  # type: ignore
# from core.auth_app.models.token import Token
# from core.auth_app.models.schemas.token import TokenSchema

# from typing import Any
# # from core.auth_app.models.schemas import TokenObtainSchema
# from core.auth_app.payloads.token import TokenService
# import logging

# # from core import loggerRequest as logger  # type: ignore

# # from ninja_jwt.token_blacklist import OutstandingToken
# logger = logging.getLogger(__name__)

# User = get_user_model()

# class TokenService:
#     """
#     Service class for managing token generation and refresh logic.
#     """

#     @staticmethod
#     def _validate_token_user(token_schema: TokenObtainSchema) -> Any:
#         """
#         Validates the token schema to check if the user exists in the database,
#         updates the token if necessary, or returns the old token.

#         Parameters:
#         - token_schema (TokenObtainSchema): Data schema with user credentials or token payload.

#         Returns:
#         - TokenSchema: A token schema containing user data and tokens if validation is successful.
#         """
#         try:
#             # Use the schema to validate and process the token response
#             response = token_schema.output_schema()

#             # Log the obtained token data for debugging and tracking
#             loggerAPI.info("Validated token schema successfully.", **response.dict())

#             return response
#         except Exception as e:
#             # Log the error if validation fails
#             loggerAPI.error("Token schema validation failed: %s", str(e))
#             raise ValidationError({"detail": str(e)})


#     @staticmethod
#     def _generate_token_metadata(user: User) -> dict:  # type: ignore
#         """
#         Generate token metadata such as access, refresh tokens, and expiration times.

#         Args:
#             user (User): The user object.

#         Returns:
#             dict: Metadata containing tokens and expiration details.
#         """
#         access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
#         refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME

#         return {
#             "access_token": AccessToken.for_user(user),
#             "refresh_token": RefreshToken.for_user(user),
#             "access_expiration": timezone.now() + access_token_lifetime,
#             "refresh_expiration": timezone.now() + refresh_token_lifetime,
#         }

#     @staticmethod
#     def get_or_create_tokens(_payload: TokenSchema) -> TokenDataSchema:  # type: ignore
#         """
#         Generate or update access and refresh tokens for a user.

#         Args:
#             user: The user for whom tokens are being created.

#         Returns:
#             TokenDataSchema: The generated token data.
#         """
#         token_metadata = TokenService._generate_token_metadata(_payload)

#         # Generate unique keys and secrets
#         key = token_hex(16)
#         token_secret = token_hex(16)

#         # Update or create the token entry in the database
#         token_entry, _ = Token.objects.update_or_create(
#             user=user,
#             defaults={
#                 "token": str(token_metadata["access_token"]),
#                 "refresh_token": str(token_metadata["refresh_token"]),
#                 "secret": token_secret,
#                 "expires_at": token_metadata["access_expiration"],
#             },
#         )

#         return TokenDataSchema(
#             token=str(token_metadata["access_token"]),
#             key=key,
#             token_secret=token_secret,
#             expiration_datetime=token_metadata["access_expiration"],
#             refresh_token=str(token_metadata["refresh_token"]),
#             refresh_token_expiration_datetime=token_metadata["refresh_expiration"],
#         )

#     @staticmethod
#     def refresh_token(refresh_token_str: str) -> TokenDataSchema:
#         """
#         Handle refreshing a token.

#         Args:
#             refresh_token_str: The provided refresh token string.

#         Returns:
#             TokenDataSchema: The newly created token data.
#         """
#         try:
#             refresh = RefreshToken(refresh_token_str)
#             user_id = refresh["user_id"]
#             user = User.objects.get(pk=user_id)

#             # Generate new tokens and update the database
#             return TokenService.get_or_create_tokens(user)
#         except User.DoesNotExist:
#             raise AuthenticationError("User not found")
#         except Exception as e:
#             raise AuthenticationError(f"Error refreshing token: {str(e)}")


# # # Example Usage in Controller
# # def get_tokens_for_user(user: User) -> TokenDataSchema:
# #     """
# #     Public method to fetch tokens for a user, using the TokenService.

# #     Args:
# #         user (User): The user object.

# #     Returns:
# #         TokenDataSchema: Generated token data.
# #     """
# #     return TokenService.get_or_create_tokens(user)


# # def refresh_user_token(refresh_token: str) -> TokenDataSchema:
# #     """
# #     Public method to refresh tokens for a user, using the TokenService.

# #     Args:
# #         refresh_token (str): The refresh token string.

# #     Returns:
# #         TokenDataSchema: New token data.
# #     """
# #     return TokenService.refresh_token(refresh_token)
