from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apis"
    verbose_name = _("APIs")
    label = "apis"
