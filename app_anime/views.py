# 前台用户动漫视图
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.shortcuts import render
from app_anime.models import Anime
from app_type.models import Type
from app_rate.models import Rate
from utils.utils import Constant, Utils, DBRoundUtils


# 前台用户动漫列表视图函数
def lists(request):
    page = request.POST.get("page", 1)  # 参数：请求页面，默认第一页
    animename = request.POST.get("animename", "")  # 参数：动漫名称
    typeid = request.POST.get("typeid", "")  # 参数：动漫类型id
    # 分页查询动漫：关联动漫类型分页查询所有动漫数据，带查询条件参数，id降序
    # 定义查询参数字典
    query_params = {}
    if animename != "":
        # 添加查询条件：动漫名称模糊查询，icontains不区分大小写，contains区分大小写
        query_params["animename__icontains"] = animename
    if typeid != "":
        typeid = int(typeid)  # 数据类型转换
        # 添加查询条件：动漫类型id
        query_params["typeid"] = typeid
    # 查询
    animes = Anime.objects.select_related("typeid").filter(**query_params).order_by("-id")
    # 分页
    paginator = Paginator(animes, Constant.page_size_user)
    pageBean = paginator.page(page)
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    # 返回到页面的数据
    return_data = {
        "page": page,
        "pageBean": pageBean,
        "types": types,
        "animename": animename,
        "typeid": typeid,
    }
    # 分页展示整理
    return_data = Utils().arrangePageBean(pageBean, return_data)
    return render(request, "anime/list.html", context=return_data)


# 前台用户动漫详情视图函数
def detail(request):
    # 通过get请求获取动漫id，是其他页面（首页、动漫列表、评分列表页面等）直接跳转到动漫详情页面
    # 通过post请求获取动漫id，是在动漫详情页面中的评分请求中获取
    animeid = request.GET.get("animeid", request.POST.get("animeid"))
    # 查询当前动漫，关联动漫类型
    anime = Anime.objects.select_related("typeid").get(id=animeid)
    # 查询当前动漫的平均评分（保留一位小数）和评分数量
    scoreCountAvgDict = Rate.objects.filter(animeid_id=animeid). \
        aggregate(scorecount=Count("id"), avgscore=DBRoundUtils(Avg("score")))
    # 相关推荐，查找与当前动漫相同的动漫类型下平均评分较高的动漫，同时排除当前登录用户评分过的动漫
    sql = "select m.*, t.*, round(avg(rate_score), 1) as avgscore, count(anime_id) as scorecount " \
          "from db_anime m " \
          "left join db_type t on type_id = anime_typeid " \
          "left join db_rate on rate_animeid = anime_id " \
          "where anime_typeid = %s and anime_id != %s " % (anime.typeid_id, animeid)
    # 判断用户是否登录
    if request.session.get(Constant.session_user, None):
        # 排除当前登录用户已评分过的动漫
        # 获取登录用户id
        userid = request.session.get(Constant.session_user).get("id")
        sql += "and anime_id not in ( select rate_animeid from db_rate where rate_userid = %s ) " % userid
    sql += "group by anime_id order by avgscore desc, scorecount desc limit 0, 5"
    print(sql)
    # 查询
    relateRecommendAnimes = Anime.objects.raw(sql)
    # 返回到页面的数据
    return_data = {
        "anime": anime,
        "scorecount": scoreCountAvgDict["scorecount"],
        "avgscore": scoreCountAvgDict["avgscore"],
        "relateRecommendAnimes": relateRecommendAnimes,
    }
    # 判断用户是否登录
    if request.session.get(Constant.session_user, None):
        # 获取登录用户id
        userid = request.session.get(Constant.session_user).get("id")
        # 查询当前登录用户是否对当前动漫评分
        rates = Rate.objects.filter(userid_id=userid, animeid_id=animeid)
        if rates is not None and len(rates) > 0:
            return_data["rate"] = rates[0]
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    return_data["types"] = types
    return render(request, "anime/detail.html", context=return_data)
