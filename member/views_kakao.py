from django.views import View
from django.shortcuts import redirect, render
from rest_framework.generics import CreateAPIView,DestroyAPIView, ListAPIView, UpdateAPIView
from django.contrib.auth.views import LoginView, LogoutView
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
from django.contrib.auth import authenticate, login, logout


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'