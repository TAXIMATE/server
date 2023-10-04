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


# 팀 세부사항
@api_view(['GET'])
def team_detail(request, team_id):
    team = Team.objects.get(pk = team_id)
    data = TeamDetailSerializer(team).data
    user = request.user
    if team.master_member == user or team.usual_member == user:
        exist_member = True
    else:
        exist_member = False
    data = dict(data)
    data.update({"state" : team.state})
    data.update({"exist_member" : exist_member})
    res = {
        "msg" : "게시글 자세한 정보 불러오기 성공",
        "code" : "t-S005",
        "data" : data,
        # "state" : team.state,
        # "exist_member" : exist_member
    }
    return Response(res)


# 유저가 속한 팀 반환
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def user_in_team(request):
    user = request.user
    now = datetime.now()
    team = Team.objects.filter((Q(master_member = user)|Q(usual_member = user))&Q(start_time__gt = now)&Q(state__not = 3)).first()
    if team is not None:
        serializer = TeamSimpleSerializer(team)
        if team.master_member == user:
            master = True
        else:
            master = False
        res = {
            "msg" : "사용자의 팀 반환 성공",
            "code" : "t-S012",
            "data" : {
                "team_data" : serializer.data,
                "master" : master
            }
        }
        return Response(res)
    res = {
        "msg" : "사용자가 속한 팀 없음",
        "code" : "t-S014"
    }
    return Response(res)