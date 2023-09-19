from django.urls import path
from . import views, views_kakao
from .views import *

app_name = 'member'

urlpatterns = [
    # path('kakao/', KakaoView.as_view()),
    # path('login/', KakaoCallBackView.as_view()),
    path('login/', views.kakao_login, name = 'kakao_login'),
    path('logout/', views.kakao_logout, name = 'kakao_logout'),
    path('gender/<str:gender>/', views.check_gender, name = 'check_gender'),
    # path('gender/', views.check_gender),
    # path('login/', views_kakao.CustomLoginView.as_view(), name='login'),
    # path('custom-login/', views_kakao.custom_login, name='custom_login'),
    # path('logout/', views_kakao.custom_logout, name='logout'),
    # path('kakao-login/', views_kakao.kakao_login, name='kakao_login'),
    # path('kakao-login/callback/', views_kakao.kakao_login_callback, name='kakao_login_callback'),
]