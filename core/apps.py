from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"
    label = "core"

    # path = "src/core"

    ## has signals for create_user_profile, save_user_profile
    # it was added to the models/profile.py file instead of here
    # def ready(self):
    #     pass
