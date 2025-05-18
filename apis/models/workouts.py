from django.db import models
from django.db.models import Count
from ._manager import WorkoutManager
from core.models import DefaultBase
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .stats import Stat
from django.db import transaction


class Workout(DefaultBase):
    title = models.CharField(max_length=255)
    date = models.DateField()

    notes = models.TextField(blank=True, null=True)
    workout_type = models.CharField(
        max_length=50,
        choices=[
            ("strength", "Strength"),
            ("cardio", "Cardio"),
            ("flexibility", "Flexibility"),
            ("balance", "Balance"),
            ("endurance", "Endurance"),
        ],
        default="strength",
    )

    objects = WorkoutManager()

    def __str__(self):
        return self.title

    @classmethod
    def get_profile_workouts(cls, profile):
        """
        Get all workouts for a given profile.
        """
        workouts = cls.objects.filter(exercises__profile=profile).annotate(total_exercises=Count("exercises"))
        return workouts


@receiver([post_save, post_delete, ], sender=Workout)
def update_stats(sender, instance: Workout, **kwargs):
    # Check if profile exists
    if not instance.profile:
        return

    # Use transaction to ensure consistency
    with transaction.atomic():
        # Re-fetch total workouts for this profile
        total_workouts = Workout.objects.filter(profile=instance.profile).count()

        # Update or create the corresponding Stat record
        stat, created = Stat.objects.get_or_create(profile=instance.profile)
        stat.total_workouts = total_workouts  # Assuming this is the intended field
        stat.save(update_fields = ["total_workouts"])
