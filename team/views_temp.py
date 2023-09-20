from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def waiting_team(request):
    data = {
        "msg" : "전체 팀 수 조회에 성공",
        "code" : "t-S001",
        "data" : {
            "teams" : 12345
        },
    }
    return Response(data)


@api_view(['POST'])
def create_team(request):
    data = {
        "msg" : "팀 생성 성공",
        "code" : "t-S002",
        "data" : {
            "team_id" : 1
        }
    }
    return Response(data)


@api_view(['POST'])
def participate_team(request, team_id):
    data = {
        "msg" : "팀 참가 성공",
        "code" : "t-S003",
        "data" : {
            "team_id" : 1
        }
    }
    return Response(data)


@api_view(['GET'])
def team_detail(request, team_id):
    data = {
        "msg" : "게시글 자세한 정보 불러오기 성공",
        "code" : "t-S005",
        "data" : {
            "start_station" : "청량리역",
            "arrival_station" : "회기역",
            "start_date" : "2023-09-20",
            "start_time" : "09:09",
            "current_member" : 3,
            "maximum_member" : 4,
            "master_memer" : {
                "nickname" : "신정섭1",
                "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
                "gender" : True,
                "temperature" : 36.5
            },
            "usual_member" : [
                {
                    "nickname" : "신정섭2",
                    "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
                    "gender" : False,
                    "temperature" : 36.4
                },
                {
                    "nickname" : "신정섭3",
                    "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
                    "gender" : True,
                    "temperature" : 100.0
                }
            ],
        "state" : 0,
        "exist_member" : True
        }
    }
    return Response(data)


@api_view(['GET'])
def get_comments(request, team_id):
    data = {
        "msg" : "전체 댓글 불러오기 성공",
        "code" : "t-S006",
        "data" : [
            {
            "nickname" : "신정섭1",
            "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
			"comment" : "롤ㄱ?",
			"created_at" : "09:09"
            },
            {
            "nickname" : "신정섭2",
            "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
			"comment" : "ㄱㄱ",
			"created_at" : "09:10"
            }
        ]
    }
    return Response(data)


@api_view(['POST'])
def create_comment(request, team_id):
    data = {
        "msg" : "댓글 작성 성공",
        "code" : "t-S007"
    }
    return Response(data)


@api_view(['GET'])
def search_team(requst):
    data = {
        "msg" : "역 이름으로 팀 검색 성공",
        "code" : "t-S008",
        "data" : [
            {
                "team_id" : 1,
                "start_station" : "회기역",
                "arrival_station" : "청량리역",
                "current_member" : 2,
                "maximum_member" : 4
            },
            {
                "team_id" : 2,
                "start_station" : "여기역",
                "arrival_station" : "저기역",
                "current_member" : 1,
                "maximum_member" : 3
            }
        ]
    }
    return Response(data)