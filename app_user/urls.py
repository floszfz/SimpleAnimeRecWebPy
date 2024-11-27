# 前台用户副路由配置文件
from django.urls import path
from app_user import views

urlpatterns = [
    path('detail', views.detail),  # 前台用户跳转到个人中心路由
    path('update', views.update),  # 前台用户跳转到用户修改页面路由
    path('doUpdate', views.doUpdate),  # 前台用户修改信息路由
    path('updatePassword', views.updatePassword),  # 前台用户跳转到修改密码页面路由
    path('doUpdatePassword', views.doUpdatePassword),  # 前台用户修改密码路由
]
