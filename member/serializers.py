from rest_framework import serializers
from .models import *
from taximate.team.models import *

# 유저의 모든 정보
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# 유저 닉네임과 사진만
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'profile_image']