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

# 현재 참가 가능한 팀 객체 리턴
def available_teams():
    now = datetime.now()
    teams = Team.objects.filter(Q(start_time__gt = now)&Q(state = 0))
    return teams



# 팀 생성
class Create_team(CreateAPIView):
    serializer_class = TeamCreateSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request):
        user = self.request.user
        now = datetime.now()
        # teams = available_teams()
        # if teams.filter(Q(usual_member = user)|Q(master_member = user)).exists():
        exist_team = Team.objects.filter(
            (Q(usual_member = user)|Q(master_member = user))
            &
            Q(start_time__gt = now)
            &
            (Q(state = 0) | Q(state = 1))
            ).first()
        if exist_team:
            res = {
                "msg" : "이미 팀에 소속된 사용자",
                "code" : "t-F005",
                "data" : {
                    "team_id" : exist_team.pk
                }
            }
            return Response(res)
        time_str = request.data.get("start_time")
        now = datetime.now()
        start_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        if now >= start_time:
            res = {
                "msg" : "잘못된 시간 입력",
                "code" : "t-F009"
            }
            return Response(res)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # team = Team.objects.get(master_member = user)
        # team_id = TeamIDSerializer(team).data["id"]
        team_id = serializer.data["id"]
        team = Team.objects.get(pk = team_id)
        team.start_time = team.start_time.strftime('%Y-%m-%dT%H:%M')
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


# 팀 취소
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def cancel_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    if team.master_member != request.user:
        res = {
            "msg" : "master_member가 아닌 사용자",
            "code" : "t-F007"
        }
    else:
        team.state = 3
        team.save()
        res = {
            "msg" : "모집 취소 성공",
            "code" : "t-S010",
        }
    return Response(res)





# 팀 참가
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def participate_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = request.user
    now = datetime.now()
    
    ## 방에 참여한 인원일 경우 (방에서 퇴장하는 경우)
    if team.master_member == user or team.usual_member.filter(kakao_id = user.kakao_id).exists():
        ## 방장일 경우
        if team.master_member == user:
            team.state = 3
            res = {
                "msg" : "방장이 팀 탈퇴, 팀 해산",
                "code" : "t-S003",
                "data" : {
                    "is_master" : True
                }
            }
        else:
            team.usual_member.remove(user)
            team.current_member -= 1
            res = {
                "msg" : "사용자 팀 퇴장",
                "code" : "t-S004",
                "data" : {
                    "is_master" : False
                }
            }
        team.save()
        return Response(res)
    
    ## 방에 참여하지 않은 인원일 경우 (방에 참여하려는 경우)
    ## 이미 다른 방에 참여한 인원일 경우
    exist_team = Team.objects.filter(
            (Q(usual_member = user)|Q(master_member = user))
            &
            Q(start_time__gt = now)
            &
            ~Q(state = 3)).first()
    if exist_team:
        res = {
            "msg" : "이미 팀에 소속된 사용자",
            "code" : "t-F003",
            "data" : {
                "team_id" : exist_team.pk
            }
        }
        return Response(res)
    ## 방 인원이 모두 찼을 경우
    if team.current_member >= team.maximum_member:
        res = {
            "msg" : "팀 인원 초과",
            "code" : "t-F004"
        }
        return Response(res)
    ## 팀에 성공적으로 참가할 경우
    team.usual_member.add(user)
    team.current_member += 1
    team.save()
    res = {
        "msg" : "팀에 성공적으로 참가",
        "code" : "t-S015",
        "data" : {
            "team_id" : team.pk
        }
    }
    return Response(res)



# 팀 출발 상태로 변경
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def team_start(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = request.user
    if team.master_member != user:
        res = {
            "msg" : "master_member가 아닌 사용자",
            "code" : "t-F006"
        }
    else:
        team.state = 1
        team.save()
        res = {
            "msg" : "팀 출발 완료",
            "code" : "t-S009"
        }
    return Response(res)


# 팀 도착 상태로 변경
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def team_arrive(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = request.user
    if team.master_member != user:
        res = {
            "msg" : "master_member가 아닌 사용자",
            "code" : "t-F006"
        }
    else:
        team.state = 2
        team.save()
        res = {
            "msg" : "팀 도착 완료",
            "code" : "t-S018"
        }
    return Response(res)