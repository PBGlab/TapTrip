from django.urls import path
from . import views

urlpatterns = [
    path('', views.home2, name='home2'), # 根路由作為首頁
    path('home', views.home, name='home'), # 登入後首頁
]