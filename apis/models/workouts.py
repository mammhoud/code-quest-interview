from django.db import models
from django.db.models import Count
from ._manager import WorkoutManager

class Workout(models.Model):
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
        workouts = cls.objects.filter(exercises__profile=profile)\
        .annotate(total_exercises=Count("exercises"))\
        
        return workouts
