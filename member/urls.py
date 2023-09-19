from django.urls import path
from . import views, views_kakao
from .views import *

app_name = 'member'

urlpatterns = [
    path('login/', views,kakao_login, name = 'kakao_login'),
    path('logout/', views.kakao_logout, name = 'kakao_logout'),
    path('gender/<str:gender>/', views.check_gender, name = 'check_gender'),
    path('information/', views.user_information, name = 'user_information'),
]