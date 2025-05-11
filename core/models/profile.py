from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .base import DefaultBase

User = get_user_model()


class Profile(DefaultBase):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=60, blank=True, null=True)
    profile_image = models.ImageField(default="default-avatar.svg", upload_to="users/", null=True, blank=True)
    cover_image = models.ImageField(default="default-cover.png", upload_to="users/", null=True, blank=True)
    language = models.CharField(
        max_length=50,
        choices=[("en", "English"), ("es", "Spanish"), ("fr", "French"), ("ar", "Arabic")],
        default="en",
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"{self.user.first_name} {self.user.last_name}"
            if self.user.first_name and self.user.last_name
            else "Profile for " + str(self.user)
        )

    class Meta:
        verbose_name_plural = _("Profile")
        verbose_name = _("User Profile")
        db_table = "Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass
