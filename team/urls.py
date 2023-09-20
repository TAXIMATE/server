from django.urls import path
from . import views, views_temp
from .views import *

app_name = 'team'

urlpatterns = [
    path('', views_temp.waiting_team),
    path('create/', views_temp.create_team),
    path('participate/<int:team_id>/', views_temp.participate_team),
    path('detail/<int:team_id>/', views_temp.team_detail),
    path('detail/comments/<int:team_id>/', views_temp.get_comments),
    path('detail/comments/create/<int:team_id>/', views_temp.create_comment),
    path('search/', views_temp.search_team),
]