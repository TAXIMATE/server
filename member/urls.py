from django.urls import path
from . import views, views_temp
from .views import *

app_name = 'member'

urlpatterns = [
    path('login/<str:code>/', views.kakao_login),
    path('logout/', views.kakao_logout),
    path('gender/<str:gender>/', views_temp.check_gender),
    path('information/', views_temp.member_information),
    path('rate/information/<int:team_id>/', views_temp.rate_member_information),
    path('rate/reflect/<int:member_id>/', views_temp.rate_reflect),
]