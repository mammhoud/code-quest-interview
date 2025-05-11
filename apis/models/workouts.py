from django.db import models


class Workout(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    exercises = models.ManyToManyField("Exercise", related_name="workouts")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
