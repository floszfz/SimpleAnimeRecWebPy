# 前台用户首页视图
from django.core.paginator import Paginator
from django.shortcuts import render
from app_anime.models import Anime
from app_rate.models import Rate
from app_type.models import Type
from utils.recommend_util import doCFBasedUser
from utils.utils import Constant, Utils


# 前台用户首页视图函数
def index(request):
    # 动漫列表：关联动漫类型分页查询所有动漫数据，动漫id降序
    animes = Anime.objects.select_related("typeid").order_by("-id")
    # 分页
    paginator = Paginator(animes, Constant.page_size_user)
    # 查询第一页
    pageBean = paginator.page(1)
    # 查询所有动漫类型：id降序排列
    types = Type.objects.all().order_by("-id")
    print("***推荐动漫开始***")
    # 判断用户是否登录
    if request.session.get(Constant.session_user, None):
        # 获取登录用户id
        userid = request.session.get(Constant.session_user).get("id")
        # 为你推荐
        recommendAnimeList = doRecommend(userid)
    else:
        print("用户未登录，采用高分推荐!")
        recommendAnimeList = getHotRecommend()
    print("***推荐动漫结束***")
    # 返回到页面的数据
    return_data = {
        "page": 1,
        "pageBean": pageBean,
        "types": types,
        "recommendAnimeList": recommendAnimeList,
    }
    # 分页展示整理
    return_data = Utils().arrangePageBean(pageBean, return_data)
    return render(request, "index/index.html", context=return_data)


# 为你推荐：
# 游客（用户未登录）：高分推荐（推荐用户平均评分较高的动漫）；
# 用户（用户已登录）：基于用户的协同过滤推荐算法，根据用户评分数据，
# 如果基于用户的协同过滤推荐算法没有推荐结果（冷启动和数据稀疏性问题造成没有推荐结果），
# 采用高分推荐（推荐用户平均评分较高的动漫）。
def doRecommend(userid):
    # 查询所有评分数据
    rates = Rate.objects.all()
    # 调用基于用户的协同过滤推荐算法
    recommendAnimeids = doCFBasedUser(userid, rates)
    # 判断是否有推荐结果
    if recommendAnimeids and len(recommendAnimeids) > 0:
        # 根据预测评分值降序查询推荐的动漫
        # 将推荐的动漫id列表转动漫id字符串（以逗号分割），动漫id列表中的id是int类型，故需先使用内置函数map将int转str
        animeids = ",".join(map(str, recommendAnimeids))
        # 根据预测评分值降序查询动漫列表sql
        sql = "select m.* from db_anime m where anime_id in (%s) order by field(anime_id, %s)" % (animeids, animeids)
        print(sql)
        # 查询
        recommendAnimeList = Anime.objects.raw(sql)
    else:
        print("基于用户的协同过滤推荐算法没有推荐结果，采用高分推荐！")
        recommendAnimeList = getHotRecommend(userid)
    return recommendAnimeList


# 高分推荐：
# 查询用户评分较高的动漫，同时排除当前登录用户已有评分数据的动漫。
# 参数userid：登录用户id，排除登录用户已有评分的动漫。
def getHotRecommend(userid=None):
    # sql语句
    sql = "select m.*, t.*, round(avg(rate_score), 1) as avgscore, count(anime_id) as scorecount " \
          "from db_anime m " \
          "left join db_type t on type_id = anime_typeid " \
          "left join db_rate on rate_animeid = anime_id " \
          "where 1 = 1 "
    # 判断用户是否登录
    if userid:  # 登录用户
        # 排除登录用户已有评分的动漫
        sql += "and anime_id not in ( select rate_animeid from db_rate where rate_userid = %s ) " % userid
    sql += "group by anime_id order by avgscore desc, scorecount desc limit 0, 10"
    print(sql)
    # 查询
    return Anime.objects.raw(sql)
