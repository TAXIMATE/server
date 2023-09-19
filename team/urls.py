from django.urls import path
from . import views
from .views import *

app_name = 'team'

urlpatterns = [
    path('create/', CreateTeam.as_view()),
]