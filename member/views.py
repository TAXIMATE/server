from django.views import View
from django.shortcuts import redirect, render
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
import json
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from social_django.utils import psa

# Create your views here.
# class KakaoView(View):
#     def get(self, request):
#         kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
#         redirect_uri = "http://127.0.0.1:8000/member/login/"
#         # redirect_uri = "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/"
#         client_id = "d679f25e59dbc97619baf1256489b449"

#         return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


# class KakaoCallBackView(View):
#     def get(self, request):
#         data = {
#             "grant_type" : "authorization_code",
#             "client_id" : "d679f25e59dbc97619baf1256489b449",
#             "redirect_uri" : "http://127.0.0.1:8000/member/login/",
#             # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
#             "code" : request.GET["code"]
#             # "code" : json.loads(request.body).get("code")
#         }

#         kakao_token_api = "https://kauth.kakao.com/oauth/token"
#         # access_token = requests.post(kakao_token_api, data = data).json()["access_token"]
#         response = requests.post(kakao_token_api, data=data)
#         res_data = response.json()
#         access_token = res_data.get("access_token")

#         kakao_user_api = "https://kapi.kakao.com/v2/user/me"
#         header = {"Authorization":f"Bearer ${access_token}"}
#         user_information = requests.get(kakao_user_api, headers = header).json()
        
#         kakao_id = user_information["id"]
#         # kakao_email = user_information["kakao_account"]["email"]
#         profile_image = user_information["kakao_account"]["profile"]["thumbnail_image_url"]
#         nickname = user_information["properties"]["nickname"]

#         if User.objects.filter(kakao_id = kakao_id).exists():
#             user = User.objects.get(kakao_id = kakao_id)
#             request.session['access_token'] = access_token
#             request.session.modified = True
#             return Response(True, status = status.HTTP_200_OK)
#         else:
#             # user = User(kakao_id = kakao_id, kakao_email = kakao_email, profile_image = profile_image, nickname = nickname)
#             user = User(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
#             user.save()
#             request.session['access_token'] = access_token
#             request.session.modified = True
#             # auth.login(request, user)
#             return Response(False, status = status.HTTP_200_OK)
        

# @api_view(['POST'])
# def logout(request):
#     auth.logout(request)
#     return Response(status = status.HTTP_200_OK)


# def logout(request):
#     kakao_admin_key = "17aff4f8209625d0480d6157aba94404"
#     logout_url = "https://kapi.kakao.com/v1/user/logout"
#     target_id = request.user.kakao_id
#     headers = {"Authorization": f"KakaoAK {kakao_admin_key}"}
#     data = {"target_id_type": "user_id", "target_id": target_id}
#     logout_res = requests.post(logout_url, headers=headers, data=data).json()
#     logout(request)

# def kakao_logout(request):
#     client_id = "d679f25e59dbc97619baf1256489b449",
#     redirect_uri = "http://127.0.0.1:8000/",
    
#     access_token = request.session.get("access_token")
# 	# 로그아웃 
#     headers = {"Authorization": f'Bearer {access_token}'}
#     logout_response = requests.post('https://kapi.kakao.com/v1/user/logout', headers=headers)
#     auth.logout(request)
#     # print(logout_response.json())

# class KakaoCallBackView(View):
#     def get(self, request):
#         data = {
#             "grant_type" : "authorization_code",
#             "client_id" : "d679f25e59dbc97619baf1256489b449",
#             "redirect_uri" : "http://127.0.0.1:8000/member/login/",
#             # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
#             "code" : request.GET["code"]
#             # "code" : json.loads(request.body).get("code")
#         }

#         kakao_token_api = "https://kauth.kakao.com/oauth/token"
#         # access_token = requests.post(kakao_token_api, data = data).json()["access_token"]
#         response = requests.post(kakao_token_api, data=data)
#         res_data = response.json()
#         access_token = res_data.get("access_token")

#         kakao_user_api = "https://kapi.kakao.com/v2/user/me"
#         header = {"Authorization":f"Bearer ${access_token}"}
#         user_information = requests.get(kakao_user_api, headers = header).json()
        
#         kakao_id = user_information["id"]
#         # kakao_email = user_information["kakao_account"]["email"]
#         profile_image = user_information["kakao_account"]["profile"]["thumbnail_image_url"]
#         nickname = user_information["properties"]["nickname"]

#         # user = auth.authenticate(request = request, kakao_id = kakao_id)
#         user = CustomUser.objects.filter(kakao_id = kakao_id).first()
#         if user is not None:
#             login(request, user=user)
#             return Response(True)
#         else:
#             new_user = CustomUser(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
#             new_user.save()
#             login(request, new_user)
#             return Response(False)

@api_view(['POST'])
def kakao_login(request, code):
    data = {
        "grant_type" : "authorization_code",
        "client_id" : "d679f25e59dbc97619baf1256489b449",
        "redirect_uri" : "http://localhost:3000/wait",
        # "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
        # "redirect_uri" : "http://127.0.0.1:8000/member/login/",
        # "code" : request.GET["code"]
        "code" : code
        # "code" : json.loads(request.body).get("code")
    }

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    # access_token = requests.post(kakao_token_api, data = data).json()["access_token"]
    response = requests.post(kakao_token_api, data=data)
    res_data = response.json()
    access_token = res_data.get("access_token")

    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    header = {"Authorization":f"Bearer ${access_token}"}
    user_information = requests.get(kakao_user_api, headers = header).json()
    
    kakao_id = user_information["id"]
    # kakao_email = user_information["kakao_account"]["email"]
    profile_image = user_information["kakao_account"]["profile"]["thumbnail_image_url"]
    nickname = user_information["properties"]["nickname"]

    # user = auth.authenticate(request = request, kakao_id = kakao_id)
    user = CustomUser.objects.filter(kakao_id = kakao_id).first()
    if user is not None:
        login(request, user=user)
        return Response(True)
    else:
        new_user = CustomUser(kakao_id = kakao_id, profile_image = profile_image, nickname = nickname)
        new_user.save()
        login(request, new_user)
        return Response(False)
        

# def kakao_logout(request):
#     user = CustomUser(request.user)
#     kakao_admin_key = "17aff4f8209625d0480d6157aba94404"
#     logout_url = "https://kapi.kakao.com/v1/user/logout"
#     target_id_type = "user_id"
#     target_id = user.kakao_id
#     headers = {"Authorization" : f"KakaoAK${kakao_admin_key}"}
#     data = {
#         "target_id_type" : target_id_type,
#         "target_id" : target_id
#     }
#     logout_res = requests.post(logout_url, headers=headers, data=data).json()
#     response = logout_res.get("id")
#     if target_id != response:
#         return Exception("Logout Failed")
#     else:
#         print("Logout Complete")
#     logout(request)
#     return Response(status = status.HTTP_200_OK)

@api_view(['POST'])
def kakao_logout(request):
    user = CustomUser(request.user)
    kakao_admin_key = "17aff4f8209625d0480d6157aba94404"
    logout_url = "https://kapi.kakao.com/v1/user/logout"
    target_id = user.kakao_id
    headers = {"Authorization" : f"KakaoAK ${kakao_admin_key}"}
    data = {
        "target_id_type" : "user_id",
        "target_id" : target_id
    }
    logout_res = requests.post(logout_url, headers=headers, data=data).json()
    response_id = logout_res.get("id")
    if response_id == target_id:
        auth.logout(request)
        return Response(status = status.HTTP_200_OK)
    else:
        return HttpResponse(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_gender(request, gender):
    user = CustomUser(request.user)
    # gender = request.data['gender']
    if gender == "male":
        user.gender = True
    elif gender == "female":
        user.gender = False
    else:
        return HttpResponse({'Wrong Request'})
    return Response(status = status.HTTP_200_OK)