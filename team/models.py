from django.db import models
from member.models import CustomUser

# Create your models here.
class Team(models.Model):
    master_member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='master_member')
    usual_member = models.ManyToManyField(CustomUser, related_name='usual_member', null = True)
    start_station = models.CharField(max_length=100, blank=True)
    arrival_station = models.CharField(max_length=100, blank=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    current_member = models.IntegerField(default=1)
    maximum_member = models.IntegerField()
    state = models.IntegerField(default=0) ## 0: 모집중, 1: 운행중, 2: 도착완료, 3: 모집취소


class Comment(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=100, blank = True)
    created_at = models.TimeField(auto_now_add=True)