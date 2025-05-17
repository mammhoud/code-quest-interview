from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

UNFOLD = {
    "SITE_TITLE": "Index Panel",
    "SITE_HEADER": "Starter Panel",
    "SITE_SUBHEADER": "ADMIN PANEL",
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [  # Supported icon set: https://fonts.google.com/icons
                    {
                        "title": _("Apis Docs (Swagger)"),
                        "icon": "dashboard",
                        "link": "/docs/swagger",
                    },
                    {
                        "title": _("Apis Docs (Redoc)"),
                        "icon": "people",
                        "link": reverse_lazy("redoc"),
                    },
                ],
            },
        ],
    },
}
