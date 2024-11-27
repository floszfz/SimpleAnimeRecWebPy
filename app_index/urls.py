# 前台用户首页副路由配置文件
from django.urls import path
from app_index import views

urlpatterns = [
    path('', views.index),  # 前台用户首页路由
    path('index', views.index),  # 前台用户首页路由
]

