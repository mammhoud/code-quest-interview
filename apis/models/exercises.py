from django.db import models
from core.models import DefaultBase
from django.utils.translation import gettext_lazy as _
from ._manager import ExerciseManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .stats import Stat
from django.db import transaction


class Exercise(DefaultBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text=_("Duration in minutes"), blank=True, null=True)
    profile = models.ForeignKey(
        "core.Profile", on_delete=models.CASCADE, related_name="exercises", blank=True, null=True
    )
    workouts = models.ManyToManyField("Workout", related_name="exercises", blank=True)

    objects = ExerciseManager()

    def __str__(self):
        return self.name


@receiver([post_save, post_delete, ], sender=Exercise)
def update_stats(sender, instance, **kwargs):
    if not instance.profile:
        return
    # Use transaction to ensure consistency
    with transaction.atomic():
        if instance.profile:
            stat = Stat.objects.filter(profile=instance.profile)
            total_ex = Exercise.objects.filter(profile=instance.profile).count()
            stat.update(total_exercises=total_ex)
