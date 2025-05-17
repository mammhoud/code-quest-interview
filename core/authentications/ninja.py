from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer
from pprint import pprint
from core.models import Token, Profile
from .. import coreLogger as logger
from django.utils.timezone import now


class GlobalAuth(HttpBearer):
    secret_header = "x-hell-secret"

    def authenticate(self, request, token_str):
        """
        1. Log the endpoint.
        2. Lookup & validate the Token.
        3. Ensure it matches the Profile.primary token.
        4. Attach user & profile to request.
        """
        # Log endpoint being accessed
        segments = request.path.strip("/").split("/")
        path_segment = segments[1] if len(segments) > 1 else ""
        logger.info(f"[Auth] Path: {path_segment}, Token: {token_str[:8]}...")
        # todo related to path_segment update the token.usage
        # todo check at each request if the requset path is the same of usage

        # Fetch token record
        token = Token.objects.filter(token=token_str, is_deleted=False).first()
        if not token:
            logger.warning("[Auth] Token not found")
            return None

        # Check validity
        if not token.is_valid():
            logger.warning(f"[Auth] Token {token.jti} invalid or expired")
            return None

        # Resolve user and profile
        user = token.created_by
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            logger.error(f"[Auth] No profile for user {user.id}")
            return None

        # **New check**: incoming token must match the profile's primary refresh
        if profile.token_id != token.jti:
            if token.token_type == token.REFRESH:
                logger.warning(f"[Auth] Token {token.jti} is not the user's primary refresh token")
                return None
            if token.token_type == token.ACCESS:
                ## todo add a check for access token and its profile - > primary_token (profile contains its parent)
                pass

        # Attach to request ,
        # Could be accessed at permission class with the same keyword (*) ,
        # and at controller by context.*request

        request.user = user
        request.profile = profile
        request.token = token
        headers = request.headers
        user_secret = headers.get(self.secret_header)
        if user_secret:
            token.secret = token._generate_secret()
            token.save(update_fields=["secret"])

        logger.info(f"[Auth] User {user.username} authenticated with primary token {token.jti}")

        token.last_used = now()
        token.save(update_fields=["last_used"])
        return token
