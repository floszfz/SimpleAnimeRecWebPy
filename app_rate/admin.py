from django.contrib import admin
from utils.utils import Constant
from app_rate.models import Rate


# 后台管理员评分管理类
@admin.register(Rate)  # 将评分模型类加入后台管理员
class RateAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = ['userid', 'animeid', 'score', 'addtime']
    # 列表页面的搜索框搜索字段：用户名、动漫名称（模糊搜索）
    search_fields = ['userid__uname', 'animeid__animename']
    # 列表页面字段添加链接，取消所有链接，禁用修改功能
    list_display_links = None
    # 列表页面每页展示的数量
    list_per_page = Constant.page_size_admin
    # 列表页面的过滤器过滤字段，可按照评分值查询
    list_filter = ('score',)

    # 禁用添加功能
    def has_add_permission(self, request):
        return False
