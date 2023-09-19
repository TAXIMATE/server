from rest_framework import serializers
from .models import *
from team.models import Team

# 유저의 모든 정보
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# 대기방에서 보여줄 유저 정보
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image', 'gender', 'temperature']