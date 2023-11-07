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
from operator import attrgetter

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
@authentication_classes([JWTAuthentication])
def search_team(request):
    request_data = request.data
    start_lst = request_data.get('start_station', [])
    arrival_lst = request_data.get('arrival_station', [])

    teams = available_teams()
    
    if start_lst == [] and arrival_lst == []:
        data = TeamSearchSerializer(teams, many = True).data
    elif start_lst and arrival_lst:
        data = []
        for team in teams:
            for s in start_lst:
                if s in team.start_station:
                    for a in arrival_lst:
                        if a in team.arrival_station:
                            data.append(TeamSearchSerializer(team).data)
                            break
                    break
    elif start_lst and not arrival_lst:
        data = []
        for team in teams:
            for s in start_lst:
                if s in team.start_station:
                    data.append(TeamSearchSerializer(team).data)
                    break
    else:
        data = []
        for team in teams:
            for a in arrival_lst:
                if a in team.arrival_station:
                    data.append(TeamSearchSerializer(team).data)
                    break

    if data == []:
        res = {
            "msg" : "조건에 맞는 팀 없음",
            "code" : "t-S010"
        }
    else:
        data = [dict(TeamSearchSerializer().to_internal_value(i)) for i in data]

        data.sort(key = lambda x : x['start_time'])

        for t in data:
            t['start_time'] = datetime.strftime(t['start_time'], "%H:%M")
        res = {
            "msg" : "역 이름으로 팀 검색 성공",
            "code" : "t-S008",
            "data" : data
        }
    return Response(res)