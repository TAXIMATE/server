from rest_framework import serializers
from .models import *
from team.models import *

# 유저 모든 정보
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['kakao_id', 'kakao_email', 'nickname', 'profile_image', 'team']

# 유저 닉네임과 사진만
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'profile_image']