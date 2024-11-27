# 前台用户动漫副路由配置文件
from django.urls import path
from app_anime import views

urlpatterns = [
    path('lists', views.lists),  # 前台用户动漫列表路由
    path('detail', views.detail),  # 前台用户动漫详情路由
]
