from django.urls import path
from . import views, views_dev
from .views import *
from .views_dev import *

app_name = 'team'

urlpatterns = [
    path('', views.waiting_teams),
    # path('create/', views.create_team),
    path('create/', Create_team.as_view()),
    path('delete/<int:team_id>/', views.destroy_team),
    path('participate/<int:team_id>/', views.participate_team),
    path('detail/<int:team_id>/', views.team_detail),
    path('detail/comments/<int:team_id>/', views.get_comments),
    path('detail/comments/create/<int:team_id>/', views.create_comment),
    path('search/', views.search_team),
    path('start/<int:team_id>/', views.team_start),
    path('own/', views.user_in_team),

    ## 개발자용 api
    path('all/', views_dev.all_teams),
]