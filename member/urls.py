from django.urls import path
from . import views, views_dev
from .views import *
from .views_dev import *

app_name = 'member'

urlpatterns = [
    path('login/<str:code>/', views.kakao_login),
    path('logout/', views.kakao_logout),
    path('gender/<str:gender>/', views.check_gender),
    path('information/', views.user_information),
    # path('test/', views.test),
    path('rate/information/<int:team_id>/', views.rate_information),
    
    ## 개발자용 api
    path('kakao/', KakaoView.as_view()),
    path('login/', views_dev.kakao_login_dev),
    path('all/', views_dev.all_member),
]