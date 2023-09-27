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


# 팀 생성 시리얼라이저
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'master_member', 'start_station', 'arrival_station', 'start_time', 'maximum_member']


# 팀 자세한 시리얼라이저
class TeamDetailSerializer(serializers.ModelSerializer):
    master_member = UserSimpleSerializer()
    usual_member = UserSimpleSerializer(many = True)
    class Meta:
        model = Team
        fields = ['start_station', 'arrival_station' , 'start_time', 'maximum_member', 'current_member', 'master_member', 'usual_member']


class TeamIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id']

class CommentCreateSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['member', 'team', 'comment']

    def create(self, validated_data):
        # validated_data에서 필요한 데이터 추출
        team = validated_data['team']
        member = validated_data['member']

        # 새로운 팀 댓글 객체 생성 및 저장
        comment = Comment(team=team, member=member)
        comment.save()

        return comment


class CommentSerializer(serializers.ModelSerializer):
    member = UserCommentSerializer()
    class Meta:
        model = Comment
        fields = ['member', 'comment', 'created_at']


class TeamCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many = True)
    class Meta:
        model = Team
        fields = ['comments']