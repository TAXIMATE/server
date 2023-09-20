from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def check_gender(request, gender):
    if gender == "male":
        data = {
            "msg" : "남성 선택",
            "code" : "m-S004",
        }
    elif gender == "female":
        data = {
            "msg" : "여성 선택",
            "code" : "m-S005",
        }
    return Response(data)

@api_view(['GET'])
def member_information(request):
    data = {
        "msg" : "유저 정보 불러오기 성공",
        "code" : "m-S006",
        "data" : {
            "nickname" : "신정섭",
            "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg",
            "gender" : True,
            "temperature" : 36.5
        }
    }
    return Response(data)

@api_view(['GET'])
def rate_member_information(request, team_id):
    data = {
        "msg" : "평가 대상 유저 정보 불러오기 성공",
        "code" : "m-S007",
        "data" : [
            {
                "member_id" : 1,
                "nickname" : "신정섭1",
                "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg"
            },
            {
                "member_id" : 2,
                "nickname" : "신정섭2",
                "profile_image" : "http://k.kakaocdn.net/dn/SFcu0/btr4tO8NIVk/Mqxpi06LIiCm0q0ObDeNBk/img_110x110.jpg"
            },
        ]
    }
    return Response(data)


@api_view(['POST'])
def rate_reflect(request, member_id):
    data = {
        "msg" : "유저 평가 반영 성공",
        "code" : "m-S008"
    }
    return Response(data)