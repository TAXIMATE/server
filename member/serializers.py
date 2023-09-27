from rest_framework import serializers
from .models import *
# from team.models import Team

# 유저의 모든 정보
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['kakao_id', 'profile_image', 'nickname', 'gender', 'temperature']

# 대기방에서 필요한 유저 정보
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image', 'gender', 'temperature']


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'nickname']


class UserRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['kakao_id', 'nickname', 'profile_image']