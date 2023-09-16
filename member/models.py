from django.db import models
from team.models import *

# Create your models here.
class User(models.Model):
    kakao_id = models.CharField(max_length=100)
    kakao_email = models.CharField(max_length=100)
    profile_image = models.TextField(default="", null = True)
    nickname = models.CharField(max_length=100)
    team = models.ForeignKey(Team, null = True)