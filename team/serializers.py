from rest_framework import serializers
from .models import *

# 팀의 모든 정보
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


# 팀의 도착/출발역, 현재/최대 인원수
class TeamSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['start_station', 'arrival_station', 'maximum_member', 'current_member']