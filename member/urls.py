from django.urls import path
from . import views
from .views import *

app_name = 'member'

urlpatterns = [
    path('login/', KakaoCallBackView.as_view()),
    path('logout/', views.logout),
    path('gender/', views.check_gender),
]