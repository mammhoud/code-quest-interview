from django.conf import settings
from django.db import models
from django.utils import timezone

# from django.utils.text import slugify
# from core.base.models.serializers.slugify import slugify
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.db import models


class DefaultBase(models.Model):
    """
    An abstract base model that provides automatic creation and update timestamps.
    """

    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_user",
        blank=True,
        verbose_name=_("Created By User"),
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, "name"):
                self.slug = slugify(self.name, "%(class)s")  # type: ignore
            elif hasattr(self, "title"):
                self.slug = slugify(self.title, "%(class)s")  # type: ignore
            else:
                self.slug = slugify(self.__str__(), "%(class)s")
        super().save(*args, **kwargs)
