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