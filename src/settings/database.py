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


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
