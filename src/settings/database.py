from src.env import env
from . import BASE_DIR

USE_SQLITE = env("USE_SQLITE", default="False") == "True"

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DB_NAME = env("DB_NAME", default="postgres")
    DB_USER = env("DB_USERNAME", default="postgres")
    DB_PASS = env("DB_PASS", default="postgres")
    DB_HOST = env("DB_HOST", default="localhost")
    DB_PORT = env("DB_PORT", default=5432)
    ENVIRONMENT = env("ENVIRONMENT", default="dev")

    # Optional (for logging or display)
    PGDATA = f"/data/{DB_NAME}-{ENVIRONMENT}"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }


CACHES_PORT = env("CACHES_PORT", default=6379)
CACHES_HOST = env("CACHES_HOST", default="localhost")
CACHES_DB = env("CACHES_DB", default=1)
CACHES_NAME = env("CACHES_NAME", default="redis")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{CACHES_NAME}://{CACHES_HOST}:{CACHES_PORT}",
        # "OPTIONS": {
        #     # "CLIENT_CLASS": "django_redis.client.DefaultClient",
        #     # "TIMEOUT": 60 * 60 * 24,  # 1 day
        # },
    }
}
GRAPHENE = {"SCHEMA": "django_root.schema.schema"}
