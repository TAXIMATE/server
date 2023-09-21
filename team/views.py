from django.views import View
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView,DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from member.models import *
from member.serializers import *
from django.db.models import Q
import requests
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json


@api_view(['GET'])
def waiting_teams(request):
    num = Team.objects.all().count()
    res = {
        "msg" : "전체 팀 수 조회에 성공",
        "code" : "t-S001",
        "data" : {
            "teams" : num
        },
    }
    return Response(res)


class Create_team(CreateAPIView):
    serializer_class = TeamCreateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def create(self, request):
        user = self.request.user
        if Team.objects.filter(Q(master_member = user)|Q(usual_member = user)).exists():
            res = {
                "msg" : "이미 팀에 소속된 사용자",
                "code" : "t-F005"
            }
            return Response(res)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        team = Team.objects.get(master_member = user)
        team_id = TeamIDSerializer(team).data["id"]
        res = {
            "msg" : "팀 생성 성공",
            "code" : "t-S002",
            "data" : {
                "team_id" : team_id
            }
        }
        return Response(res)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(master_member = user)


@api_view(['DELETE'])
def destroy_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    team.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def all_teams(request):
    teams = Team.objects.all()
    serializer = TeamSimpleSerializer(teams, many = True)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def participate_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    if team.master_member == request.user:
        res = {
            "msg" : "방장은 팀 참가 불가",
            "code" : "t-F004"
        }
        return Response(res)

    # 팀 인원 초과시
    if team.current_member == team.maximum_member:
        res = {
            "msg" : "팀 인원 초과",
            "code" : "t-F003",
        }
        return Response(res)
    
    # 팀 탈퇴시
    if team.usual_member.filter(kakao_id = request.user.kakao_id).exists():
        team.usual_member.remove(request.user)
        team.current_member -= 1
        res = {
            "msg" : "팀 탈퇴 성공",
            "code" : "t-S004"
        }
    # 팀 참가시
    else:
        team.usual_member.add(request.user)
        team.current_member += 1
        res = {
            "msg" : "팀 참가 성공",
            "code" : "t-S003",
            "data" : {
                "team_id" : int
            }
        }
    team.save()
    return Response(res)


@api_view(['GET'])
def team_detail(request, team_id):
    team = Team.objects.get(pk = team_id)
    data = TeamDetailSerializer(team).data
    res = {
        "msg" : "게시글 자세한 정보 불러오기 성공",
        "code" : "t-S005",
        "data" : data
    }
    return Response(res)