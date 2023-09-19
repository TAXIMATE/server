from django.views import View
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView,DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from member.models import *
from member.serializers import *
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.db.models import Q
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
@api_view(['GET'])
def number_of_team(request):
    number = Team.objects.all().count()
    data = {
        "teams" : number
    }
    return Response(data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_team(request):
    serializer = TeamCreateSerializer(data = request.data, master_member = request.user)
    if serializer.is_valid():
        serializer.save()
        Response(status = status.HTTP_200_OK)
    Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def participate_team(request, team_id):
    team = Team.objects.get(pk = team_id)
    user = CustomUser(request.user)
    if team.usual_member.filter(pk = user.pk).exists():
        team.usual_member.remove(user)
        team.current_member -= 1
    else:
        team.usual_member.add(user)
        team.current_member += 1
    team.save()
    return Response(status = status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def team_detail(request, team_id):
    team = Team.objects.get(pk = team_id)
    serializer = TeamDetailSerializer(team)
    return Response