from rest_framework import serializers
from .models import *
from taximate.member.models import *
from taximate.member.serializers import *

# 팀의 모든 정보
class TeamDetailSerializer(serializers.Serializer):
    class Meta:
        model = Team
        fields = '__all__'


# 팀의 도착/출발역, 현재/최대 인원수
class TeamSimpleSerializer(serializers.Serializer):
    class Meta:
        model = Team
        fields = ['start_station', 'arrival_station', 'maximum_member', 'current_member']