from django.views import View
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView,DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from member.models import *
from member.serializers import *
from rest_framework.decorators import api_view
from django.db.models import Q
import requests

# Create your views here.
class CreateTeam(CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer