from datetime import timedelta


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ipuq)$7$z^$*@c)&^+m-j2*s62@vvjc!0yw2bh)vjovfi-4b6x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


## refrence
# https://github.com/twtrubiks/django_jwt_tutorial/blob/master/django_jwt_tutorial/settings.py
# docs: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,  # Set to True to rotate refresh tokens it was created for make token changes after every request
    "BLACKLIST_AFTER_ROTATION": False,  # Set to True to blacklist the old refresh token after a new one is issued and false of u need to use it again after a while
    "UPDATE_LAST_LOGIN": False,  # Set to True to update the last login field of the user when the token is issued ##
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",), # The type of the token in the Authorization header, (default: Bearer), (e.g. "Authorization"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",  # JWT ID / ex: "jti": "a1b2c3d4e5f6g7h8i9j0",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
