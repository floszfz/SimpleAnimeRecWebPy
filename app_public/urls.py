# 前台用户公共副路由配置文件
from django.urls import path
from app_public import views

urlpatterns = [
    path('login', views.login),  # 跳转到前台用户登录页面路由
    path('register', views.register),  # 跳转到前台用户注册页面路由
    path('doLogin', views.doLogin),  # 前台用户登录路由
    path('doRegister', views.doRegister),  # 前台用户注册路由
    path('forgetPassword', views.forgetPassword),  # 跳转到前台用户忘记密码页面路由
    path('doForgetPassword', views.doForgetPassword),  # 前台用户重置忘记的密码路由
    path('logout', views.logout),  # 前台用户退出登录路由
    path('upload', views.upload),  # 前台用户文件上传路由
]
