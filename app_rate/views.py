# 前台评分视图
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from app_rate.models import Rate
from app_type.models import Type
from utils.utils import Constant, Utils


# 前台评分列表视图函数
def lists(request):
    page = request.POST.get("page", 1)  # 参数：请求页面，默认第一页
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询当前用户的评分记录，关联动漫，id降序
    rates = Rate.objects.select_related("animeid").filter(userid_id=userid).order_by("-id")
    paginator = Paginator(rates, Constant.page_size_user)  # 分页
    pageBean = paginator.page(page)
    # 返回到页面的数据
    return_data = {
        "pageBean": pageBean,
        "page": page,
    }
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    return_data["types"] = types
    # 分页展示整理
    return_data = Utils().arrangePageBean(pageBean, return_data)
    return render(request, "rate/list.html", context=return_data)


# 前台用户添加或修改评分视图函数
def doSaveOrUpdate(request):
    post = request.POST  # 请求方式：post
    animeid = post.get("animeid")  # 参数：动漫id
    score = post.get("score")  # 参数：评分值
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    # 查询评分记录
    rates = Rate.objects.filter(animeid_id=animeid, userid_id=userid)
    if rates is not None and len(rates) > 0:
        # 评分已存在，更新
        rate = rates[0]
        rate.score = int(score)
        rate.save()
    else:  # 添加评分记录
        rate = Rate()  # 定义评分模型类
        rate.userid_id = userid  # 用户id
        rate.animeid_id = animeid  # 动漫id
        rate.score = int(score)  # 评分值
        rate.addtime = Utils().getCurrentTime()  # 评分时间
        rate.save()  # 保存
    # 返回到页面的数据
    return_data = {
        "success": 1,  # 1：操作成功
        "toUrl": "reload"  # reload：重新加载请求的页面
    }
    return JsonResponse(return_data)


# 前台用户删除评分视图函数
def doDelete(request):
    rateid = request.POST.get("rateid")  # 参数：评分id
    # 从session会话中获取当前登录用户的id
    userid = request.session.get(Constant.session_user).get("id")
    if rateid is not None and rateid != "":
        Rate.objects.filter(id=rateid, userid_id=userid).delete()  # 删除
    # 返回到页面的数据
    return_data = {
        "success": 1,  # 1：操作成功
        "toUrl": "reload"  # reload：重新加载请求的页面
    }
    return JsonResponse(return_data)
