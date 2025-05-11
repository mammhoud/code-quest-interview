from django.db import models




class Record(models.Model):
    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="records")
    friend = models.ForeignKey(
        "Friend", on_delete=models.SET_NULL, null=True, blank=True, related_name="records"
    )
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE, related_name="records")
    date = models.DateField()
    performance = models.CharField(max_length=255)

    def __str__(self):
        return f"Record for {self.profile} on {self.date}"
