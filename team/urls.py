from django.urls import path
from . import views
from .views import *

app_name = 'team'

urlpatterns = [
    path('', views.number_of_team),
]