from django.db import models
from member.models import *

# Create your models here.
class Team(models.Model):
    master_member = models.ForeignKey(User, on_delete=models.CASCADE)
    start_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    current_member = models.IntegerField(default=1)
    maximum_member = models.IntegerField()
