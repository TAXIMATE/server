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
from django.http import JsonResponse

# Create your views here.
class KakaoView(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        # redirect_uri = "http://127.0.0.1:8000/member/login/"
        redirect_uri = "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/"
        client_id = "d679f25e59dbc97619baf1256489b449"

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoCallBackView(View):
    def get(self, request):
        data = {
            "grant_type" : "authorization_code",
            "client_id" : "d679f25e59dbc97619baf1256489b449",
            # "redirect_uri" : "http://127.0.0.1:8000/member/login/",
            "redirect_uri" : "https://port-0-server-2rrqq2blmoc3kpx.sel5.cloudtype.app/member/login/",
            "code" : request.GET["code"]
            # "code" : json.loads(request.body).get("code")
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        # access_token = requests.post(kakao_token_api, data = data).json()["access_token"]
        response = requests.post(kakao_token_api, data=data)
        res_data = response.json()
        access_token = res_data.get("access_token")

        kakao_user_api = "http://kapi.kakao.com/v2/user/me"
        header = {"Authorization":f"Bearer ${access_token}"}
        user_information = requests.get(kakao_user_api, headers = header).json()
        
        kakao_id = user_information.get["id"]
        kakao_email = user_information["kakao_account"]["email"]
        profile_image = user_information["properties"]["profile"]["profile_image_url"]
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

def kakao_logout(request):
    access_token = request.session.get('kakao_access_token')

    if access_token:
        # 카카오 로그아웃 요청을 보냅니다.
        kakao_logout_url = 'https://kapi.kakao.com/v1/user/logout'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.post(kakao_logout_url, headers=headers)

        if response.status_code == 200:
            # 카카오 로그아웃이 성공한 경우, 세션에서 카카오 액세스 토큰을 삭제합니다.
            del request.session['kakao_access_token']
            return JsonResponse({'message': '카카오 로그아웃이 성공적으로 처리되었습니다.'})
    
    return JsonResponse({'error': '카카오 로그아웃에 실패하였습니다.'}, status=400)

@api_view(['POST'])
def check_gender(request):
    user = request.user
    user.gender = request.json()["gender"]
    return Response(status = status.HTTP_200_OK)