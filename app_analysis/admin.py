from django.contrib import admin
from app_analysis.models import Analysis
from utils.utils import SqlQueryUtils


# 后台管理员数据分析管理类
@admin.register(Analysis)  # 将Analysis类加入后台管理员
class AnalysisModelAdmin(admin.ModelAdmin):
    # 重定义列表页面
    change_list_template = 'admin/analysis/list.html'

    # 重写列表页面视图函数
    def changelist_view(self, request, extra_context=None):
        # 调用父类的列表页面视图函数，获取返回对象response
        response = super().changelist_view(request, extra_context=extra_context)
        # 数据分析
        # sql语句，用户性别统计
        sql = "select user_gender, count(user_gender) as usercount from db_user group by user_gender"
        print(sql)
        # 查询
        usergenderList = SqlQueryUtils().sql_query_all(sql)
        # sql语句，查询所有动漫类型的平均评分
        # mysql内置函数round()：四舍五入并保留一位小数，返回float数据类型，django接收查询结果后，float类型会转为decimal类型，
        # 但是我们需要字符串类型可直接输出，故再需要使用mysql内置函数convert()转字符串，但是排序需要使用float类型
        sql = "select type_id, type_typename, " \
              "convert(round(avg(rate_score), 1), char) as avgscore, count(anime_id) as scorecount " \
              "from db_rate " \
              "left join db_anime on rate_animeid = anime_id " \
              "left join db_type on anime_typeid = type_id " \
              "group by type_id " \
              "order by round(avg(rate_score), 1) desc, type_id desc"
        print(sql)
        # 查询
        animetypeList = SqlQueryUtils().sql_query_all(sql)
        # 返回到页面的数据
        response.context_data['usergenderList'] = usergenderList
        response.context_data['animetypeList'] = animetypeList
        return response

    # 禁用添加功能
    def has_add_permission(self, request):
        return False
