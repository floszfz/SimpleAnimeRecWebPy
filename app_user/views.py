# 前台用户视图
from django.http import JsonResponse
from django.shortcuts import render
from app_type.models import Type
from app_user.models import User
from utils.utils import Constant


# 前台用户跳转到个人中心视图函数
def detail(request):
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询用户
    user = User.objects.get(id=userid)
    # 返回到页面的数据
    return_data = {
        "user": user,
    }
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    return_data["types"] = types
    return render(request, "user/detail.html", context=return_data)


# 前台用户跳转到用户修改页面视图函数
def update(request):
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询用户
    user = User.objects.get(id=userid)
    # 返回到页面的数据
    return_data = {
        "user": user,
    }
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    return_data["types"] = types
    return render(request, "user/update.html", context=return_data)


# 前台用户修改信息视图函数
def doUpdate(request):
    post = request.POST  # 请求方式：post
    uname = post.get('uname')  # 参数：用户名
    fullname = post.get('fullname')  # 参数：姓名
    phone = post.get('phone')  # 参数：电话
    mailbox = post.get('mailbox')  # 参数：邮箱
    age = post.get('age')  # 参数：年龄
    gender = post.get('gender')  # 参数：性别
    headpic = post.get("headpic")  # 参数：头像
    introduction = post.get("introduction")  # 参数：个人简介
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询新用户名是否已经存在，用户名唯一
    # 查询参数：新用户名、用户id，exclude是排除条件
    users = User.objects.filter(uname=uname).exclude(id=userid)
    if users is not None and len(users) > 0:
        message = "用户名已存在！"
    else:
        # 更新
        success = User.objects.filter(id=userid).\
            update(uname=uname, fullname=fullname, mailbox=mailbox,
                   phone=phone, gender=gender, age=age, headpic=headpic, introduction=introduction)
        if success > 0:  # 操作成功，更新session会话中登录用户信息
            # 查询用户
            user = User.objects.get(id=userid)
            # 将登录用户信息保存到session会话中
            request.session[Constant.session_user] = user.convert_dict()
    # 返回到页面的数据
    return_data = {
        "success": success,
        "message": message,
        "toUrl": "reload",  # reload：重新加载请求的页面
    }
    return JsonResponse(return_data)


# 前台用户跳转到修改密码页面视图函数
def updatePassword(request):
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询用户
    user = User.objects.get(id=userid)
    # 返回到页面的数据
    return_data = {
        "user": user,
    }
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    return_data["types"] = types
    return render(request, "user/updatePassword.html", context=return_data)


# 前台用户修改密码视图函数
def doUpdatePassword(request):
    post = request.POST  # 请求方式：post
    oldPassword = post.get("oldPassword")  # 参数：旧密码
    newPassword = post.get("newPassword")  # 参数：新密码
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    toUrl = ""  # 操作结果返回的toUrl
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询用户
    user = User.objects.get(id=userid)
    # 判断旧密码是否正确
    if user.password == oldPassword:
        # 更新密码
        success = User.objects.filter(id=userid).update(password=newPassword)
        if success > 0:
            toUrl = "login"  # 操作成功跳转到前台用户登录页面
            message = "操作成功！请重新登陆！"
            # 删除session会话信息
            del request.session[Constant.session_user]
    else:
        message = "旧密码不正确！"
    # 返回到页面的数据
    return_data = {
        "success": success,
        "message": message,
        "toUrl": toUrl
    }
    return JsonResponse(return_data)
