from django.contrib import admin
from django.utils.safestring import mark_safe
from app_anime.models import Anime
from utils.utils import Constant, Utils


# 后台管理员动漫管理类
@admin.register(Anime)  # 将动漫模型类加入后台管理员
class AnimeAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = ['animename', 'typeid', 'addtime']
    # 列表页面的搜索框搜索字段：动漫名称（模糊搜索）
    search_fields = ['animename']
    # 列表页面每页展示的数量
    list_per_page = Constant.page_size_admin
    # 列表页面的过滤器过滤字段，可按照动漫类型查询
    list_filter = ('typeid__typename',)
    # 编辑页面需要编辑的字段
    fields = ["animename", "typeid", "showImage", "pic", "weburl", "introduction"]
    # 编辑页面的只读字段
    readonly_fields = ["showImage"]

    # 编辑页面，格式化展示动漫图片
    def showImage(self, obj):
        try:
            # 输出动漫图片html代码
            imageHtml = mark_safe('<img src="%s" width="80px" />' % obj.pic.url)
        except Exception as e:
            imageHtml = ''
        return imageHtml

    # 设置字段显示的标题
    showImage.short_description = "动漫图片"

    # 重写添加或者修改方法
    def save_model(self, request, obj, form, change):
        # 如果是添加操作
        if not change:
            # 设置添加时间
            obj.addtime = Utils().getCurrentTime()
        super().save_model(request, obj, form, change)
