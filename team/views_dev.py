from rest_framework.response import Response
from .serializers import *
from .models import *
from member.models import *
from member.serializers import *
from rest_framework.decorators import api_view

# 모든 팀 목록
@api_view(['GET'])
def all_teams(request):
    teams = Team.objects.all()
    serializer = TeamSimpleSerializer(teams, many = True)
    return Response(serializer.data)