# 前台用户公共视图
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from SimpleAnimeRecWebPy import settings
from app_user.models import User
from utils.utils import Constant, Utils


# 跳转到前台用户登录页面视图函数
def login(request):
    return render(request, "login.html")


# 前台用户登录视图函数
def doLogin(request):
    post = request.POST  # 请求方式：post
    uname = post.get('uname')  # 参数：用户名
    password = post.get('password')  # 参数：密码
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    toUrl = ""  # 操作结果返回的toUrl
    # 查询
    users = User.objects.filter(uname=uname, password=password)
    if users is not None and len(users) > 0:
        currentUser = users[0]  # 获取当前登录用户对象
        # 将登录用户信息保存到session会话中
        request.session[Constant.session_user] = currentUser.convert_dict()
        # 登录成功跳转到前台首页
        toUrl = "index"
        success = 1
    else:
        message = "操作失败！用户名或密码错误！"
    # 返回到页面的数据
    return_data = {
        "success": success,
        "message": message,
        "toUrl": toUrl
    }
    return JsonResponse(return_data)


# 跳转到前台用户注册页面视图函数
def register(request):
    return render(request, "register.html")


# 前台用户注册视图函数
def doRegister(request):
    post = request.POST  # 请求方式：post
    uname = post.get('uname')  # 参数：用户名
    password = post.get('password')  # 参数：密码
    phone = post.get('phone')  # 参数：电话
    mailbox = post.get('mailbox')  # 参数：邮箱
    age = post.get('age')  # 参数：年龄
    gender = post.get('gender')  # 参数：性别
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    toUrl = ""  # 操作结果返回的toUrl
    # 查询用户名是否已经存在
    users = User.objects.filter(uname=uname)
    if users is not None and len(users) > 0:
        message = "操作失败！用户名已存在！"
    else:
        user = User()  # 实例化用户模型对象
        user.uname = uname  # 用户名
        user.password = password  # 密码
        user.phone = phone  # 电话
        user.mailbox = mailbox  # 邮箱
        user.age = age  # 年龄
        user.gender = gender  # 性别
        user.headpic = Constant.header_default_user  # 设置默认头像
        user.addtime = Utils().getCurrentTime()  # 注册时间
        user.save()  # 保存
        success = 1
        toUrl = "login"  # 跳转到前台用户登录页面
    # 返回到页面的数据
    return_data = {
        "success": success,
        "message": message,
        "toUrl": toUrl
    }
    return JsonResponse(return_data)


# 跳转到前台用户忘记密码页面视图函数
def forgetPassword(request):
    return render(request, "forgetPassword.html")


# 前台用户重置忘记的密码视图函数
def doForgetPassword(request):
    post = request.POST  # 请求方式：post
    uname = post.get('uname')  # 参数：用户名
    phone = post.get('phone')  # 参数：电话
    mailbox = post.get('mailbox')  # 参数：邮箱
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    toUrl = ""  # 操作结果返回的toUrl
    # 查询
    users = User.objects.filter(uname=uname, phone=phone, mailbox=mailbox)
    if users is not None and len(users) > 0:
        currentUser = users[0]  # 获取当前用户对象
        # 更新用户密码，重置为默认密码
        currentUser.password = Constant.password_default_user
        currentUser.save()  # 更新
        message = "操作成功！初始密码：" + Constant.password_default_user
        toUrl = "login"  # 跳转到登录页面
        success = 1
    else:
        message = "操作失败！用户信息不正确！"
    # 返回到页面的数据
    return_data = {
        "success": success,
        "message": message,
        "toUrl": toUrl
    }
    return JsonResponse(return_data)


# 前台用户退出登录视图函数
def logout(request):
    if not request.session.get(Constant.session_user, None):
        # 跳转到前台首页
        return redirect("/")
    # 删除session会话信息
    del request.session[Constant.session_user]
    # 跳转到前台首页
    return redirect('/')


# 前台用户文件上传视图函数
def upload(request):
    file = request.FILES.get("file")  # 获取上传的文件对象
    print(file.name)  # 上传的文件名
    fileName = file.name  # 文件名
    fileType = os.path.splitext(fileName)[1]  # 文件类型：例如：.jpg
    # 重新定义上传文件的名称，文件名称唯一：时间_随机数.文件格式
    newFileName = Utils().getCurrentTimeRandom() + fileType
    print(newFileName)
    # 上传文件保存路径
    newFilePath = os.path.join(settings.MEDIA_ROOT, newFileName)
    # 保存上传文件
    with open(newFilePath, "wb") as f:
        for line in file:
            f.write(line)
    # 返回到页面的数据
    return_data = {
        "success": 1,  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
        "newFileName": newFileName
    }
    return JsonResponse(return_data)
