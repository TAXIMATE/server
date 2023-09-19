from rest_framework import serializers
from .models import *
from team.models import Team

# 유저의 모든 정보
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# 유저 닉네임과 사진만
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        # model = User
        fields = ['nickname', 'profile_image']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        # model = User
        fields = ['gender']