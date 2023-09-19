from rest_framework import serializers
from .models import *
from member.serializers import *

# 팀의 모든 정보
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


# 팀의 도착/출발역, 현재/최대 인원수
class TeamSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'start_station', 'arrival_station', 'maximum_member', 'current_member']


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['master_member', 'start_station', 'arrival_station', 'start_date', 'start_time', 'maximum_member']


class TeamDetailSerializer(serializers.ModelSerializer):
    master_member = UserSimpleSerializer()
    usual_member = UserSimpleSerializer()
    class Meta:
        model = Team
        fields = ['start_station', 'arrival_station' , 'start_data', 'start_time', 'maximum_member', 'current_member', 'master_member', 'usual_member']