from django.db import models


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

    def __str__(self):
        return self.title
