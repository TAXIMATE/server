from django.urls import path
from team.views import *

app_name = 'team'

urlpatterns = [
    path('', waiting_teams),
    # path('create/', views.create_team),
    path('create/', Create_team.as_view()),
    path('cancel/<int:team_id>/', cancel_team),
    path('participate/<int:team_id>/', participate_team),
    path('detail/<int:team_id>/', team_detail),
    path('detail/comments/<int:team_id>/', get_comments),
    path('detail/comments/create/<int:team_id>/', create_comment),
    path('search/', search_team),
    path('start/<int:team_id>/', team_start),
    path('own/', user_in_team),

    ## 개발자용 api
    path('all/', views_dev.all_teams),
]