from django.db import models
from core.models import DefaultBase
from ._manager import StatManager


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
    total_workouts = models.IntegerField(default=0)
    total_exercises = models.IntegerField(default=0)
    evaluation = models.IntegerField(default=0)
    objects = StatManager()

    def __str__(self):
        return f"Stat: {self.profile.full_name}, {self.total_workouts} posts"
