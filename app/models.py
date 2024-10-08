from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title} - {self.message} - {self.date}"
