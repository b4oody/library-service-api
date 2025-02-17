from django.db import models

from config.settings.base import AUTH_USER_MODEL


class TelegramUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.user
