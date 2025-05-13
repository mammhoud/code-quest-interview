# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # "django.contrib.flatpages",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "django_filters",
    "django_extensions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "dj_rest_auth",
    # "dj_rest_auth.registration",
    "drf_spectacular",
    'ninja_extra',
    # "rest_framework_simplejwt", # hashed to be use dj_rest_auth because it more flexible and easy to use with django-allauth
    "graphene_django",
    "core",
    "apis",
] + [  # admin app addition tweaks { docs: https://unfoldadmin.com/docs }
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",  # required
]
