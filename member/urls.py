from django.urls import path
from . import views
from .views import *

app_name = 'member'

urlpatterns = [
    path('login/<str:code>/', views.kakao_login),
    path('logout/', views.kakao_logout),
    path('gender/<str:gender>/', views.check_gender),
    path('information/', views.user_information),
    # path('test/', views.test),
    path('rate/information/<int:team_id>/', views.rate_information),
    
    ## 개발자용 url
    path('kakao/', KakaoView.as_view()),
    path('login/', views.kakao_login_dev),
    path('all/', views.all_member),
]