from django.urls import path
from . import views
from .views import *

app_name = 'member'

urlpatterns = [
    path('kakao/', KakaoView.as_view()),
    path('login/', KakaoCallBackView.as_view()),
    path('logout/', views.kakao_logout),
    path('gender/', views.check_gender),
]