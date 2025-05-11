from django.db import models


class Friend(models.Model):
    profile = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey("core.Profile", on_delete=models.CASCADE, related_name="friend_of")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} is friends with {self.friend}"
