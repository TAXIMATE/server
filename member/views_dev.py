from django.views import View
from django.shortcuts import redirect
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
import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth import login
from decouple import config

"""
개발 편의를 위한 api
"""
# 백엔드 로그인용 api
class KakaoView(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://127.0.0.1:8000/member/login/"
        # redirect_uri = "http://localhost.3000/wait"
        # redirect_uri = "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/"
        client_id = config('client_id')

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


# 백엔드 로그인용 콜백 api
@api_view(['GET'])
def kakao_login_dev(request):
    data = {
        "grant_type" : "authorization_code",
        "client_id" : config('client_id'),
        # "redirect_uri" : "http://localhost.3000/wait",
        "redirect_uri" : "http://127.0.0.1:8000/member/login/",
        # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
        "code" : request.GET["code"]
        # "code" : code
    }

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    response = requests.post(kakao_token_api, data=data).json()
    access_token = response.get("access_token")

    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    header = {"Authorization":f"Bearer ${access_token}"}
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
            # "data" : serializer.data
            "data" : {
                "user_data" : serializer.data,
                "access_token" : access_token
            }
        }
        return Response(res)

    new_user = CustomUser(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
    new_user.save()
    serializer = UserSerializer(new_user)
    auth.login(request, new_user)
    res = {
        "msg" : "신규 가입자, 로그인 성공",
        "code" : "m-S001",
        "data" : {
            "user_data" : serializer.data,
            "access_token" : access_token
        }
    }
    return Response(res)    
        

    """
    if user is not None:
        # 프로필 사진이 바뀌었을 경우 적용
        if user.profile_image != profile_image:
            user.profile_image = profile_image
        # 닉네임이 바뀌었을 경우 적용
        if user.nickname != nickname:
            user.nickname = nickname
        user.save()
        if user.gender != None:
            auth.login(request, user=user)
            res_data = {
                "msg" : "기존 사용자 로그인 성공",
                "code" : "m-S002",
                "data" : {
                "gender_needed" : True
                }
            }
            return Response(res_data)
        else:
            auth.login(request, user = user)
            res_data = {
                "msg" : "신규 가입자 로그인 성공",
                "code" : "m-S001",
                "data" : {
                "gender_needed" : False
                }
            }
            return Response(res_data)
    new_user = CustomUser(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
    new_user.save()
    auth.login(request, new_user)
    res_data = {
        "msg" : "신규 가입자, 로그인 성공",
        "code" : "m-S001",
        "data" : {
        "gender_needed" : False
        }
    }
    return Response(res_data)
    """


# 모든 사용자 리턴
@api_view(['GET'])
def all_member(request):
    members = CustomUser.objects.all()
    serializer = UserSerializer(members, many = True)
    return Response(serializer.data)