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
    DB_HOST = env("DB_HOST", default="postgres")
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
CACHES_HOST = env("CACHES_HOST", default="redis")
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


# Redis connection
CACHEOPS_REDIS = {
    "host": CACHES_HOST,
    "port": CACHES_PORT,
    "db": 1,
    "socket_timeout": 3,
    # 'password': '********',
}

# Cacheops settings
CACHEOPS = {
    "apis.stat": {"ops": "all", "timeout": 60 * 10},
    "apis.workout": {"ops": "all", "timeout": 60 * 5},
    "apis.exercise": {"ops": "all", "timeout": 60 * 10},
    "core.token": {"ops": "all", "timeout": 60 * 10},
}

CACHEOPS_DEFAULTS = {
    "timeout": 60 * 15  # default timeout if not set above
}

# Disable admin cache if needed
CACHEOPS_DEGRADE_ON_FAILURE = True  # fallback if Redis down
