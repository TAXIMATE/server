from django.db import models
from team.models import Team
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(models.Model):
#     kakao_id = models.BigIntegerField(unique=True)
#     # kakao_email = models.CharField(max_length=100)
#     profile_image = models.TextField(default="", null = True)
#     nickname = models.CharField(max_length=100)
#     gender = models.BooleanField(null=True)
#     temperature = models.FloatField(default=36.5)
#     team = models.ForeignKey(Team, null = True, related_name="all_members", on_delete=models.SET_NULL)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, unique=False)
    user_id = models.AutoField(primary_key=True)
    kakao_id = models.BigIntegerField(unique=True)
    profile_image = models.TextField(default="", null = True)
    nickname = models.CharField(max_length=100)
    gender = models.BooleanField(null=True)
    temperature = models.FloatField(default=36.5)
    team = models.ForeignKey(Team, null = True, related_name="all_member", on_delete=models.SET_NULL)