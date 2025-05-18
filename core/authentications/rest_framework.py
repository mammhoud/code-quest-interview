from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from django.contrib.auth import get_user_model
from ..models import Token, Profile  # adjust import paths as needed
from .. import coreLogger as logger

User = get_user_model()


class GlobalAuth(BaseAuthentication):
    """
    Custom token authentication that:
      1. Parses and logs the request path.
      2. Looks up & validates our Token model.
      3. Ensures it’s the user’s primary Profile.token.
      4. Attaches both `request.user` and `request.profile`.
    """

    keyword = "Bearer"  # or 'Token' as the default
    secret_header = "x-hell-secret"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None  # no credentials provided

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(_("Invalid token header. No credentials provided."))
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. Token string should not contain spaces.")
            )

        try:
            token_str = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. Token string has invalid characters.")
            )

        # Log the path segment
        path_segments = request.path.strip("/").split("/")
        segment = path_segments[1] if len(path_segments) > 1 else ""
        logger.info(f"[Auth] DRF Path: {segment}, Token: {token_str[:8]}...")

        # Lookup token record
        token = Token.objects.filter(token=token_str, is_deleted=False).first()
        if not token:
            logger.warning("[Auth] Token not found")
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        # Validate token state
        if not token.is_valid():
            logger.warning(f"[Auth] Token {token.jti} invalid or expired")
            raise exceptions.AuthenticationFailed(_("Token expired or revoked."))

        # Resolve user & profile
        user = token.created_by
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            logger.error(f"[Auth] No profile for user {user.id}")
            raise exceptions.AuthenticationFailed(_("Profile not found."))

        # Ensure this token is the primary one for this profile
        if profile.token_id != token.jti:
            logger.warning(f"[Auth] Token {token.jti} is not the user's primary refresh token")
            raise exceptions.AuthenticationFailed(_("Token is not primary for this user."))

        # Attach to request and return
        request.user = user
        request.profile = profile
        request.auth = token
        headers = request.headers
        user_secret = headers.get(self.secret_header)

        try:
            if user_secret:
                if Token.validate_token(token.jti, user_secret):
                    token.secret = token._generate_secret()

            logger.info(f"[Auth] User {user.username} authenticated with primary token {token.jti}")

            token.last_used = now()
            token.save(update_fields=["last_used", "secret"])
        except:  # noqa: E722
            logger.error(f"[Error Auth] request didnt contains Headers ot couldnt get the secret_header var")  # noqa: F541

        logger.info(f"[Auth] User {user.username} authenticated with primary token {token.jti}")
        return (user, token)

    def authenticate_header(self, request):
        return self.keyword
