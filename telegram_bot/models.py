import uuid

from django.db import models

from config.settings.base import AUTH_USER_MODEL


class TelegramUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    unique_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user} {self.telegram_id}"
