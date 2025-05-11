from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes", blank=True, null=True)

    def __str__(self):
        return self.name
