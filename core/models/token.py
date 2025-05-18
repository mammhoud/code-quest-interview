from uuid import uuid4

from django.conf import settings
from django.db import models, transaction
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _  # type: ignore
from ninja_jwt.tokens import AccessToken, RefreshToken  # type: ignore
import logging
from datetime import timedelta as dt_timedelta
from core import coreLogger
# from ninja_jwt.token_blacklist import OutstandingToken


class Token(models.Model):  # type: ignore
    """
    Token model managing JWT creation, validation, and lifecycle.
    """

    ACCESS = "access"
    REFRESH = "refresh"
    SLIDING = "sliding" # or ROTATED
    TOKEN_TYPES = [
        (ACCESS, "Access"),
        (REFRESH, "Refresh"),
        (SLIDING, "Sliding"),
    ]

    jti = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
        verbose_name="Token ID",
    ) # id field
    token = models.TextField(null=True, blank=True)
    token_type = models.CharField(max_length=10, choices=TOKEN_TYPES)
    secret = models.CharField(max_length=64, blank=True)
    usage = models.CharField(
        max_length=20,
        choices=[("api", "API"), ("web", "Web"), ("mobile", "Mobile")],
        default="api",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tokens",
    )  # todo add created_for field if the token could be created by another user who will use it!!
    preferences = models.JSONField(default=list, blank=True) # settings field # dummy
    last_used = models.DateTimeField(null=True, blank=True) # updated on each request 
    is_revoked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    iat = models.DateTimeField(auto_now_add=True) # created at 
    exp = models.DateTimeField(null=True, blank=True) # expiration date
    saved_at = models.DateTimeField(auto_now_add=True)
    desc = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = "tokens"
        verbose_name = _("Bearer Token")
        verbose_name_plural = _("Bearer Tokens")

    def save(self, *args, **kwargs):
        # Ensure expiration and secret are set
        if not self.exp:
            default_span = (
                dt_timedelta(days=7) if self.token_type == self.REFRESH else dt_timedelta(minutes=15)
            )
            self.exp = now() + default_span
        if not self.secret:
            self.secret = get_random_string(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.token_type.title()} Token ({self.jti})"

    @property
    def profile(self):
        if self.token_type == self.REFRESH:
            if len(self.profiles.distinct()) == 1:
                return self.profiles.first()
            else:
                self.profiles.filter(id == self.created_by)
        else:
            pass
    # ------------- Validation & State -------------
    def is_valid(self):
        return not self.is_revoked and now() < self.exp

    def revoke(self):  # used at controller
        """Revoke this token and cascade if refresh."""
        self.is_revoked = True
        self.save(update_fields=["is_revoked"])
        # revoke all children tokens if this is a refresh token
        if self.token_type == self.REFRESH:
            for child in self.children.all():
                child.revoke()

    # ------------- Creation -------------
    @staticmethod
    def _generate_secret():
        return get_random_string(64)

    @classmethod
    def create_token(
        cls, profile, raw_token: str, token_type: str, parent: "Token" = None, duration: dt_timedelta = None
    ):  # used at controller # todo add token usage 
        """
        Create and persist a JWT-backed token instance.
        """
        if not token_type:
            raise ValueError("token_type is required.")
        exp_duration = (
            duration
            or (  # todo add to settings the default duration / with env var and use it here 
                dt_timedelta(minutes=15) if token_type == cls.ACCESS else dt_timedelta(days=7)
            )
        )
        obj = cls.objects.create(
            token=str(raw_token),
            token_type=token_type,
            parent=parent,
            created_by=profile.user,
            secret=cls._generate_secret(),
            exp=now() + exp_duration,
        )
        return obj
    @classmethod
    def create_access_token(cls, profile, refresh_token: "Token"):  # used at profile model
        raw = AccessToken.for_user(profile.user)  # using AccessToken class from ninja_jwt
        return cls.create_token(profile, raw, cls.ACCESS, parent=refresh_token)

    @classmethod
    def create_refresh_token(cls, profile):  # used at profile model
        """Retrieve or generate a refresh token for the profile."""
        existing = cls.objects.filter(
            parent__isnull=True,
            created_by=profile.user,
            token_type=cls.REFRESH,
            is_revoked=False,
            is_deleted=False,
        ).first()
        if existing:
            profile.token = existing
            profile.save(update_fields=["token"])
            return existing
        raw = RefreshToken.for_user(profile.user)
        token = cls.create_token(profile, raw, cls.REFRESH)
        profile.token = token
        profile.save(update_fields=["token"])
        return token

    # ------------- Query -------------
    @classmethod
    def validate_token(cls, jti, secret): # used at globalAuth
        try:
            tok = cls.objects.get(jti=jti, secret=secret, is_revoked=False, is_deleted=False)
            return tok.is_valid()
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_active_tokens(cls, user):  # used at profile model
        return cls.objects.filter(created_by=user, is_revoked=False, is_deleted=False, exp__gt=now())

    # ------------- Refresh Primary -------------
    @classmethod
    def refresh_primary_token(cls, token=None, user=None, jti=None):  # used at controller
        """Rotate primary refresh token (and re-parent children)."""
        # Ensure at least one identifier is provided
        if not any([token, user, jti]):
            coreLogger.error("Provide 'token', 'user', or 'jti'.")

        # Determine the existing primary refresh token
        if token:
            old = cls.objects.filter(
                token=token,
                token_type=cls.REFRESH,
                is_revoked=False,
                is_deleted=False,
            ).first()
            if not old:
                coreLogger.error("Invalid refresh token string.")
        elif jti:
            old = cls.objects.filter(
                jti=jti,
                token_type=cls.REFRESH,
                is_revoked=False,
                is_deleted=False,
            ).first()
            if not old:
                coreLogger.error("Invalid refresh token ID (jti).")
        else:
            old = cls.objects.filter(
                created_by=user,
                token_type=cls.REFRESH,
                is_revoked=False,
                is_deleted=False,
            ).first()
            if not old:
                coreLogger.error(f"No active refresh token for user {user}.")

        # Create a new primary refresh token tied to the same Profile
        user_profile = old.created_by.profile
        new_primary = cls.create_token(
            profile=user_profile,
            raw_token=None,
            token_type=cls.REFRESH,
        )

        # Re-parent children tokens to the new primary, then revoke the old one
        cls.objects.filter(parent=old).update(parent=new_primary)
        old.revoke()

        return new_primary
