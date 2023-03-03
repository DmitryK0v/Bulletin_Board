from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class AdvUser(AbstractUser):
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Have you been activated?")
    is_activated = False
    send_messages = models.BooleanField(default=True, verbose_name="Send notifications about new comments?")

    class Meta(AbstractUser.Meta):
        pass
