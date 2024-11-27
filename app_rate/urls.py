# 前台评分副路由配置文件
from django.urls import path
from app_rate import views

urlpatterns = [
    path('lists', views.lists),  # 前台评分列表路由
    path('doSaveOrUpdate', views.doSaveOrUpdate),  # 前台用户添加或修改评分路由
    path('doDelete', views.doDelete),  # 前台用户删除评分路由
]

