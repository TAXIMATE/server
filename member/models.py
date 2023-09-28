from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    kakao_id = models.BigIntegerField(unique=True, null = True)
    profile_image = models.TextField(default="", null = True)
    nickname = models.CharField(max_length=100, null = True)
    gender = models.BooleanField(null=True)
    temperature = models.FloatField(default=36.5)

    USERNAME_FIELD = 'kakao_id'