from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from team.models import *
# from team.models import *
# from team.serializers import *
from rest_framework.decorators import api_view, authentication_classes
from django.db.models import Q
from django.contrib import auth
import requests
from django.views import View
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from decouple import config

# Create your views here.
# 카카오 로그인
@api_view(['GET'])
def kakao_login(request, code):
    referer = request.META.get('HTTP_REFERER', '')
    if "localhost:3000" in referer:
        data = {
            "grant_type" : "authorization_code",
            "client_id" : config('client_id'),
            # "redirect_uri" : "https://taximate-nine.vercel.app/wait",
            "redirect_uri" : "http://localhost:3000/wait",
            # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
            # "code" : request.GET["code"]
            "code" : code
        }
    else:
        data = {
            "grant_type" : "authorization_code",
            "client_id" : config('client_id'),
            "redirect_uri" : "https://taximate-alpha.vercel.app/wait",
            # "redirect_uri" : "http://127.0.0.1:8000/member/login/",
            # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
            # "code" : request.GET["code"]
            "code" : code
        }

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    # access_token = requests.post(kakao_token_api, data = data).json()["access_token"]
    response = requests.post(kakao_token_api, data=data)
    res_data = response.json()
    kakao_access_token = res_data.get("access_token")

    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    header = {"Authorization":f"Bearer ${kakao_access_token}"}
    user_information = requests.get(kakao_user_api, headers = header).json()
    
    kakao_id = user_information["id"]
    profile_image = user_information["kakao_account"]["profile"]["thumbnail_image_url"]
    nickname = user_information["properties"]["nickname"]

    user = CustomUser.objects.filter(kakao_id=kakao_id).first()
    if user is not None:
        if user.profile_image != profile_image:
            user.profile_image = profile_image
        if user.nickname != nickname:
            user.nickname = nickname
        user.save()
        serializer = UserSerializer(user)
        login(request, user)
        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        res = {
            "msg" : "기존 사용자 로그인 성공",
            "code" : "m-S002",
            "data" : {
                "user_data" : serializer.data,
                "access_token" : access_token
            }
        }
        return Response(res)

    new_user = CustomUser(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
    new_user.save()
    serializer = UserSerializer(new_user)
    login(request, new_user)
    token = TokenObtainPairSerializer.get_token(new_user)
    access_token = str(token.access_token)
    res = {
        "msg" : "신규 가입자, 로그인 성공",
        "code" : "m-S001",
        "data" : {
            "user_data" : serializer.data,
            "access_token" : access_token
        }
    }
    return Response(res)   


# 성별 선택
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def check_gender(request, gender):
    if gender == "male":
        request.user.gender = "male"
        request.user.save()
        data = {
            "msg" : "남성 선택",
            "code" : "m-S004",
        }
    elif gender == "female":
        request.user.gender = "female"
        request.user.save()
        data = {
            "msg" : "여성 선택",
            "code" : "m-S005",
        }
    else:
        data = {
            "msg" : "성별 선택 오류",
            "code" : "m-F001"
        }
    return Response(data)


# 현재 유저 정보 반환
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def user_information(request):
    serializer = UserSimpleSerializer(request.user)
    data = serializer.data
    if data["nickname"] == None:
        res = {
            "msg" : "유저 정보 불러오기 실패",
            "code" : "m-F002"
        }
        return Response(res)
    res = {
        "msg" : "유저 정보 불러오기 성공",
        "code" : "m-S006",
        "data" : data
    }
    return Response(res)


# 평가할 유저 정보 반환
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def rate_information(request, team_id):
    user = request.user
    team = Team.objects.get(pk = team_id)
    master_member = team.master_member
    usual_member = team.usual_member.all()
    master_data = UserRateSerializer(master_member).data
    usual_data = UserRateSerializer(usual_member, many = True).data
    users = usual_data + [master_data]
    
    users = [u for u in users if u['kakao_id'] != user.kakao_id]
    if users == []:
        team.state = 2
        team.save()
        res = {
            "msg" : "평가 대상자 없음",
            "code" : "m-S008",
        }
    else:
        res = {
            "msg" : "평가 대상 유저 정보 불러오기 성공",
            "code" : "m-S007",
            "data" : users
        }
    return Response(res)


# class KakaoLogoutView(View):
#     def get(self, request):
#         kakao_api = "https://kauth.kakao.com/oauth/logout"
#         # redirect_uri = "http://127.0.0.1:8000/member/login/"
#         # redirect_uri = "http://localhost.3000/wait"
#         redirect_uri = "http://127.0.0.1:8000/member/logout/"
#         client_id = config('client_id')

#         return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


# 서비스 로그아웃
@api_view(['POST'])
def kakao_logout(request):
    auth.logout(request)
    data = {
        "msg" : "로그아웃 성공",
        "code" : "m-S003",
    }
    return Response(data)


# 평가 반영
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def reflect_rate(request, kakao_id):
    user = CustomUser.objects.get(kakao_id = kakao_id)
    
    res = {
        "msg" : "유저 평가 반영 성공",
        "code" : "m-S008"
    }
    return Response(res)