from django.contrib import admin
from app_type.models import Type
from utils.utils import Constant


# 后台管理员动漫类型管理类
@admin.register(Type)  # 将动漫模型类加入后台管理员
class TypeAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = ['typename']
    # 列表页面的搜索框搜索字段：动漫类型名称（模糊搜索）
    search_fields = ['typename']
    # 列表页面每页展示的数量
    list_per_page = Constant.page_size_admin
    # 编辑页面需要编辑的字段
    fields = ["typename"]
