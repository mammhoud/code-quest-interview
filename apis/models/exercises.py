from django.db import models
from core.models import DefaultBase
from django.utils.translation import gettext_lazy as _
from ._manager import WorkoutManager


class Exercise(DefaultBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text=_("Duration in minutes"), blank=True, null=True)
    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="exercises")
    workouts = models.ManyToManyField("Workout", related_name="exercises", blank=True)
    objects = WorkoutManager()

    def __str__(self):
        return self.name
