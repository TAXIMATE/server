from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(null=True, unique=False, max_length=20)
    kakao_id = models.BigIntegerField(unique=True, null = True)
    profile_image = models.TextField(default="", null = True)
    nickname = models.CharField(max_length=100, null = True)
    gender = models.BooleanField(null=True)
    temperature = models.FloatField(default=36.5)
    grade = models.CharField(max_length=20, default="silver")

    USERNAME_FIELD = 'kakao_id'

    def __str__(self):
        return self.nickname