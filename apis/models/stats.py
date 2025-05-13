from django.db import models
from core.models import DefaultBase


class Stat(DefaultBase):
    """
    Model to store statistics for the application.
    """

    profile = models.OneToOneField(
        "core.Profile",
        on_delete=models.CASCADE,
        related_name="stats",
        null=True,
        blank=True,
    )
    # total_fats = models.IntegerField(default=0)
    total_records = models.IntegerField(default=0)
    total_exercises = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)
    evaluation = models.IntegerField(default=0)

    def __str__(self):
        return f"Stat: {self.profile.full_name}, {self.total_records} posts"
