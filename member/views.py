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
import requests

# Create your views here.
# class KakaoCallBackView(View):
#     def get(self, request):
#         data = {
#             "grant_type" : "authorization_code",
#             "client_id" : "",
#             "redirect_uri" : "",
#             "code" : request.GET["code"]
#         }

#         kakao_token_api = "https://kauth.kakao.com/oauth/token"
#         access_token = requests.post