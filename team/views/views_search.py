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

# 현재 참가 가능한 팀 객체 리턴
def available_teams():
    now = datetime.now()
    teams = Team.objects.filter(Q(start_time__gt = now)&Q(state = 0))
    return teams


# 대기 중인 팀 수
@api_view(['GET'])
def waiting_teams(request):
    # now = datetime.now()
    # num = Team.objects.filter(start_time__gt = now).count()
    num = available_teams().count()
    res = {
        "msg" : "대기 중인 팀 수 조회에 성공",
        "code" : "t-S001",
        "data" : {
            "teams" : num
        },
    }
    return Response(res)


# 역 이름으로 팀 검색
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def search_team(request):
    res = request.data
    start_station = res["start_station"]
    arrival_station = res["arrival_station"]
    now = datetime.now()
    # 검색 조건
    # 출발역, 도착역, 출발시각
    teams = available_teams()
    searched_teams = teams.filter(Q(start_station__contains = start_station)&Q(arrival_station__contains = arrival_station))
    # teams = Team.objects.filter((Q(start_station__contains = start_station)&Q(arrival_station__contains = arrival_station))&Q(start_time__gt = now))
    serializer = TeamSimpleSerializer(searched_teams, many = True)
    data = serializer.data
    if data == []:
        res = {
            "msg" : "조건에 맞는 팀 없음",
            "code" : "t-S010"
        }
    else:
        res = {
            "msg" : "역 이름으로 팀 검색 성공",
            "code" : "t-S008",
            "data" : data
        }
    return Response(res)