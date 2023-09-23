from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from member.models import *
from member.serializers import *
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from datetime import datetime


# 대기 중인 팀 수
@api_view(['GET'])
def waiting_teams(request):
    now = datetime.now()
    # num = Team.objects.all().count()
    num = Team.objects.filter(start_time__gt = now).count()
    res = {
        "msg" : "대기 중인 팀 수 조회에 성공",
        "code" : "t-S001",
        "data" : {
            "teams" : num
        },
    }
    return Response(res)


# 팀 생성
class Create_team(CreateAPIView):
    serializer_class = TeamCreateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def create(self, request):
        user = self.request.user
        now = datetime.now()
        if Team.objects.filter((Q(master_member = user)|Q(usual_member = user))&Q(start_time__gt = now)).exists():
            res = {
                "msg" : "이미 팀에 소속된 사용자",
                "code" : "t-F005"
            }
            return Response(res)
        time_str = request.data.get("start_time")
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


# 팀 삭제
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def destroy_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    if team.master_member != request.user:
        res = {
            "msg" : "master_member가 아닌 사용자",
            "code" : "t-F007"
        }
    else:
        team.delete()
        res = {
            "msg" : "팀 삭제 성공",
            "code" : "t-S010",
        }
    return Response(res)


# 모든 팀 목록
@api_view(['GET'])
def all_teams(request):
    teams = Team.objects.all()
    serializer = TeamSimpleSerializer(teams, many = True)
    return Response(serializer.data)


# 팀 참가
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def participate_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = request.user
    now = datetime.now()
    
    ## 방에 참여한 인원일 경우 (방에서 퇴장하는 경우)
    if team.master_member == user or team.usual_member == user:
        ## 방장일 경우
        if team.master_member == user:
            team.delete()
            res = {
                "msg" : "방장이 팀 퇴장",
                "code" : "t-S003",
                "data" : {
                    "is_master" : True
                }
            }
        else:
            team.usual_member.remove(user)
            team.current_member -= 1
            res = {
                "msg" : "일반 사용자 팀 퇴장",
                "code" : "t-S004",
                "data" : {
                    "is_master" : False
                }
            }
        team.save()
        return Response(res)
    
    ## 방에 참여하지 않은 인원일 경우 (방에 참여하려는 경우)
    ## 이미 다른 방에 참여한 인원일 경우
    if Team.objects.filter((Q(usual_member = user)|Q(master_member = user))&Q(start_time__gt = now)).exists():
        res = {
            "msg" : "이미 팀에 소속된 사용자",
            "code" : "t-F003"
        }
        return Response(res)
    ## 방 인원이 모두 찼을 경우
    if team.current_member >= team.maximum_member:
        res = {
            "msg" : "팀 인원 초과",
            "code" : "t-F004"
        }
        return Response(res)
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
    


    ##########
    # if Team.objects.filter((Q(usual_member = user)|Q(master_member = user))&Q(start_time__gt = now)).exists():
    #     res = {
    #         "msg" : "이미 팀에 소속된 사용자",
    #         "code" : "t-F005"
    #     }
    #     return Response(res)

    # if team.master_member == request.user:
    #     res = {
    #         "msg" : "방장은 팀 참가 불가",
    #         "code" : "t-F004"
    #     }
    #     return Response(res)

    # # 팀 인원 초과시
    # if team.current_member == team.maximum_member:
    #     res = {
    #         "msg" : "팀 인원 초과",
    #         "code" : "t-F003",
    #     }
    #     return Response(res)
    
    # # 팀 탈퇴시
    # if team.usual_member.filter(kakao_id = request.user.kakao_id).exists():
    #     team.usual_member.remove(request.user)
    #     team.current_member -= 1
    #     res = {
    #         "msg" : "팀 탈퇴 성공",
    #         "code" : "t-004"
    #     }
    # # 팀 참가시
    # else:
    #     team.usual_member.add(request.user)
    #     team.current_member += 1
    #     res = {
    #         "msg" : "팀 참가 성공",
    #         "code" : "t-003",
    #         "data" : {
    #             "team_id" : int
    #         }
    #     }
    # team.save()
    # return Response(res)


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


# 댓글 작성
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
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
    teams = Team.objects.filter((Q(start_station__contains = start_station)&Q(arrival_station__contains = arrival_station))&Q(start_time__gt = now))
    serializer = TeamSimpleSerializer(teams, many = True)
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


# 팀 출발 상태로 변경
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
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


# 유저가 속한 팀 반환
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def user_in_team(request):
    user = request.user
    if Team.objects.filter(master_member = user).exists():
        team = Team.objects.get(master_member = user)
        serializer = TeamSimpleSerializer(team)
        res = {
            "msg" : "사용자의 팀 반환 성공",
            "code" : "t-S012",
            "data" : {
                "team_data" : serializer.data,
                "master" : True
            }
        }
    elif Team.objects.filter(usual_member = user).exists():
        team = Team.objects.get(usual_member = user)
        serializer = TeamSimpleSerializer(team)
        res = {
            "msg" : "사용자가 속한 팀 반환 성공",
            "code" : "t-S013",
            "data" : {
                "team_data" : serializer.data,
                "master" : False
            }
        }
    else:
        res = {
            "msg" : "사용자가 속한 팀 없음",
            "code" : "t-S014"
        }
    return Response(res)