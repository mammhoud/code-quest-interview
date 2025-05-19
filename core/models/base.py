import itertools
from django.conf import settings
from django.db import models
from django.utils import timezone

# from django.utils.text import slugify
# from core.base.models.serializers.slugify import slugify
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField,ShortUUIDField,ModificationDateTimeField

from django.db import models


class DefaultBase(models.Model):
    """
    An abstract base model that provides automatic creation and update timestamps.
    """

    slug = ShortUUIDField()
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()
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

    # @classmethod
    # def _generate_slug(cls, value):
    #     # max_length = cls._meta.get_field("slug").max_length
    #     # value = cls.title
    #     slug_candidate = slug_original = slugify(value, allow_unicode=True)
    #     for i in itertools.count(1):
    #         if not cls.objects.filter(slug=slug_candidate).exists():
    #             break
    #         slug_candidate = "{}-{}".format(slug_original, i)

    #     cls.slug = slug_candidate

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         value = ""
    #         if hasattr(self, "name"):
    #             value = self.name
    #         elif hasattr(self, "title"):
    #             value = self.title
    #         else:
    #             value = self.__str__()

    #         self.slug = DefaultBase._generate_slug(value=f"{value} + {str(self.pk)}")
    #     super().save(*args, **kwargs)
