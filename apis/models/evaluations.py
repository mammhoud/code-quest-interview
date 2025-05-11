from django.db import models


class Evaluation(models.Model):
    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="evaluations")
    date = models.DateField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Evaluation for {self.profile} on {self.date}"


class ExerciseAttendance(models.Model):
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE, related_name="attendances")
    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="exercise_attendances")
    scheduled_date = models.DateField()
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile} - {self.exercise} on {self.scheduled_date} (Attended: {self.attended})"
