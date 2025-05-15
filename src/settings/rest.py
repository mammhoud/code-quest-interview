REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # django default pre defined permissions that was created by django-rest-framework
        # extending this to add more permissions like is created by owner
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 2,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    # "DEFAULT_THROTTLE_RATES": {"anon": "2/minute", "products": "2/minute", "orders": "4/minute"},
}

# django settings.py
NINJA_EXTRA = {
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1001/day'
    },
    "NUM_PROXIES": None,
}
SPECTACULAR_SETTINGS = {
    # "AUTHENTICATION_CLASSES": (
    #     "rest_framework_simplejwt.authentication.JWTAuthentication",
    #     "rest_framework.authentication.SessionAuthentication",
    # ),
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "TITLE": "REST API",
    "DESCRIPTION": "REST API for EXAM Project Exercises and Fitness",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
