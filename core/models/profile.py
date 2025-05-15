from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .token import Token

from .base import DefaultBase


class Profile(models.Model):
    """
    Extension of User model, holding profile-specific data and token management.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=60, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="users/", default="default-avatar.svg", null=True, blank=True)
    cover_image = models.ImageField(upload_to="users/", default="default-cover.png", null=True, blank=True)
    language = models.CharField(
        max_length=50,
        choices=[("en", "English"), ("es", "Spanish"), ("fr", "French"), ("ar", "Arabic")],
        default="en",
    )
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Primary refresh token
    token = models.ForeignKey(
        "Token",
        on_delete=models.CASCADE,
        related_name="profiles",
        null=True,
        blank=True,
        help_text="Primary refresh token for the user",
    )

    class Meta:
        db_table = "profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"Profile for {self.user.username}"

    # ----------------- Token Helpers -----------------
    def get_primary_refresh(self):
        """Return the primary refresh token or None."""
        return self.token

    def set_primary_refresh(self, refresh=None):
        """
        Assign or create a primary refresh token for this profile.
        Returns the assigned Token instance.
        """
        if refresh:
            self.token = refresh
        elif not self.token:
            self.token = Token.create_refresh_token(self)
        self.save(update_fields=["token"])
        return self.token

    def create_access_token(self):
        """Generate a new access token linked to the primary refresh token."""
        primary = self.get_primary_refresh()
        if not primary or primary.token_type != Token.REFRESH:
            raise ValueError("Valid primary refresh token required.")
        return Token.create_access_token(self, primary)

    def get_all_access_tokens(self):
        """Fetch all active access tokens under the primary refresh token."""
        primary = self.get_primary_refresh()
        if not primary or primary.token_type != Token.REFRESH:
            raise ValueError("Valid primary refresh token required.")
        return Token.get_active_tokens(self.user).filter(token_type=Token.ACCESS)

    def revoke_primary(self):
        """Revoke primary refresh token and its children."""
        primary = self.get_primary_refresh()
        if primary:
            primary.revoke()
            self.token = None
            self.save(update_fields=["token"])
            return True
        return False

    def revoke_all_tokens(self):
        """Revoke all tokens (refresh & access) issued by this user."""
        tokens = Token.objects.filter(created_by=self.user)
        count = tokens.count()
        for t in tokens:
            t.revoke()
        return count


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        profile , created = Profile.objects.get_or_create(user=instance)
        if created:
            profile.full_name = f"{instance.first_name} {instance.last_name}"
            profile.token = profile.set_primary_refresh()
            profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, "profile"):
            instance.profile.full_name = f"{instance.first_name} {instance.last_name}"
            instance.profile.save()
        instance.profile.save()

    except Profile.DoesNotExist:
        pass
