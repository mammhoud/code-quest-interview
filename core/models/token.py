from uuid import uuid4

from django.conf import settings
from django.db import models, transaction
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _  # type: ignore
from ninja_jwt.tokens import AccessToken, RefreshToken  # type: ignore
import logging
from datetime import timedelta as dt_timedelta
# from core import loggerRequest as logger  # type: ignore

# from ninja_jwt.token_blacklist import OutstandingToken
logger = logging.getLogger(__name__)


class Token(models.Model):  # type: ignore
    """
    Token model managing JWT creation, validation, and lifecycle.
    """

    ACCESS = "access"
    REFRESH = "refresh"
    SLIDING = "sliding"
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
    )
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
    )
    preferences = models.JSONField(default=list, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_revoked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    iat = models.DateTimeField(auto_now_add=True)
    exp = models.DateTimeField(null=True, blank=True)
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

    # ------------- Validation & State -------------
    def is_valid(self):
        return not self.is_revoked and now() < self.exp

    def revoke(self):
        """Revoke this token and cascade if refresh."""
        self.is_revoked = True
        self.save(update_fields=["is_revoked"])
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
    ):
        """
        Create and persist a JWT-backed token instance.
        """
        if not token_type:
            raise ValueError("token_type is required.")
        exp_duration = duration or (
            dt_timedelta(minutes=15) if token_type == cls.ACCESS else dt_timedelta(days=7)
        )
        return cls.objects.create(
            token=raw_token,
            token_type=token_type,
            parent=parent,
            created_by=profile.user,
            secret=cls._generate_secret(),
            exp=now() + exp_duration,
        )

    @classmethod
    def create_access_token(cls, profile, refresh_token: "Token"):
        raw = AccessToken.for_user(profile.user)
        return cls.create_token(profile, raw, cls.ACCESS, parent=refresh_token)

    @classmethod
    def create_refresh_token(cls, profile):
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
    def validate_token(cls, jti, secret):
        try:
            tok = cls.objects.get(jti=jti, secret=secret, is_revoked=False, is_deleted=False)
            return tok.is_valid()
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_active_tokens(cls, user):
        return cls.objects.filter(created_by=user, is_revoked=False, is_deleted=False, exp__gt=now())

    # ------------- Refresh Primary -------------
    @classmethod
    def refresh_primary_token(cls, user=None, jti=None):
        """Rotate primary refresh token (and re-parent children)."""
        if user is None and jti is None:
            raise ValueError("Provide either user or jti.")
        if jti:
            old = cls.objects.filter(
                jti=jti, token_type=cls.REFRESH, is_revoked=False, is_deleted=False
            ).first()
            if not old:
                raise ValueError("Invalid refresh token.")
        else:
            old = cls.objects.filter(
                created_by=user, token_type=cls.REFRESH, is_revoked=False, is_deleted=False
            ).first()
            if not old:
                raise ValueError(f"No active refresh token for user {user}.")
        children = list(old.children.all())
        new_primary = cls.create_token(old, None, cls.REFRESH)
        # Re-parent and revoke old
        cls.objects.filter(parent=old).update(parent=new_primary)
        old.revoke()
        return new_primary
