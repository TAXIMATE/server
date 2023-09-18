from django.views import View
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView,DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
# from team.models import *
# from team.serializers import *
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib import auth
import requests

# Create your views here.
class KakaoCallBackView(View):
    def get(self, request):
        data = {
            "grant_type" : "authorization_code",
            "client_id" : "d679f25e59dbc97619baf1256489b449",
            "redirect_uri" : "http://localhost:3000/wait",
            "code" : request.GET["code"]
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token = requests.post(kakao_token_api, data = data).json()["access_token"]

        kakao_user_api = "http://kapi.kakao.com/v2/user/me"
        header = {"Authorization":f"Bearer ${access_token}"}
        user_information = requests.get(kakao_user_api, headers = header).json()

        kakao_id = user_information["id"]
        kakao_email = user_information["kakao_account"]["email"]
        profile_image = user_information["properties"]["profile_image"]
        nickname = user_information["properties"]["nickname"]

        if User.objects.get(kakao_id = kakao_id).DoesNotExist:
            user = User(kakao_id = kakao_id, kakao_email = kakao_email, profile_image = profile_image, nickname = nickname)
            user.save()
            auth.login(request, user)
            return Response(False, status = status.HTTP_200_OK)
        else:
            user = User.objects.get(kakao_id = kakao_id)
            auth.login(request, user)
            return Response(True, status = status.HTTP_200_OK)
        

@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(status = status.HTTP_200_OK)


@api_view(['POST'])
def check_gender(request):
    user = request.user
    user.gender = request.json()["gender"]
    return Response(status = status.HTTP_200_OK)