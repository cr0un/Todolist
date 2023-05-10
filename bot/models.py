import random
import string
from django.db import models
from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=100, null=True, unique=True, default=None)
    state = models.CharField(max_length=255, null=True, blank=True)

    @staticmethod
    def generate_verification_code():
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(6))
