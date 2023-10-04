from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from member.models import *
from member.serializers import *
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication

# 댓글 작성
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_comment(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = request.user
    serializer = CommentCreateSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(team = team, member = user)
        res = {
            "msg" : "댓글 작성 성공",
            "code" : "t-S007"
        }
        return Response(res)
    res = {
        "msg" : "댓글 작성 실패",
        "code" : "t-F004"
    }
    return Response(res)


# 댓글 목록 가져오기
@api_view(['GET'])
def get_comments(request, team_id):
    team = Team.objects.get(pk = team_id)
    serializer = TeamCommentsSerializer(team)
    res = {
        "msg" : "전체 댓글 불러오기 성공",
        "code" : "t-S006",
        "data" : serializer.data
    }
    return Response(res)