from enum import Enum



import environ

# Initialize environment reader
env = environ.Env()
environ.Env.read_env()  # This reads the .env file

class Environment(Enum):
    DEVELOPMENT = "dev"
    TESTING = "test"
    PRODUCTION = "prod"

# Get the current environment from .env
CURRENT_ENV = Environment(env("DJANGO_ENV", default=Environment.DEVELOPMENT.value))  # type: ignore
