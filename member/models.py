from django.db import models
from taximate.team.models import Team

# Create your models here.
class User(models.Model):
    kakao_id = models.BigIntegerField(unique=True)
    kakao_email = models.CharField(max_length=100)
    profile_image = models.TextField(default="", null = True)
    nickname = models.CharField(max_length=100)
    team = models.ForeignKey(Team, null = True, related_name="all_member")