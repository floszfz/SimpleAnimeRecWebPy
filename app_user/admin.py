from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from utils.utils import Constant
from app_user.models import User


# 后台管理员用户管理类
@admin.register(User)  # 将用户模型类加入后台管理员
class UserAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = ['uname', 'fullname', 'gender', 'age', 'addtime']
    # 列表页面的搜索框搜索字段：用户名、用户姓名（模糊搜索）
    search_fields = ['uname', 'fullname']
    # 列表页面每页展示的数量
    list_per_page = Constant.page_size_admin
    # 编辑页面需要编辑的字段
    fields = ['uname', 'fullname', 'showHeader', 'headpic', 'phone', 'mailbox',
              'age', 'gender', 'introduction']
    # 编辑页面的只读字段
    readonly_fields = ['showHeader']
    # 列表页面动作集合添加功能：重置用户密码
    actions = ['resetPassword']

    # 编辑页面，格式化展示用户头像图片
    def showHeader(self, obj):
        try:
            # 输出用户头像图片html代码
            headerHtml = mark_safe('<img src="%s" width="80px" />' % obj.headpic.url)
        except Exception as e:
            headerHtml = ''
        return headerHtml

    # 设置字段显示的标题
    showHeader.short_description = "用户头像"

    # 列表页面动作集合添加功能：重置用户密码
    def resetPassword(self, request, queryset):
        # 查询数据库，并更新用户密码为默认密码
        queryset.update(password=Constant.password_default_user)
        # 提示信息
        messages.info(request, "初始密码：%s！" % Constant.password_default_user)

    # 设置字段显示的标题
    resetPassword.short_description = "重置用户密码"

    # 重写添加或者修改方法
    def save_model(self, request, obj, form, change):
        # 如果是添加操作
        if not change:
            # 添加操作，目前管理员不支持添加用户操作
            messages.error(request, "操作失败！")
            messages.set_level(request, messages.ERROR)
        else:  # 修改
            # 调用父类修改方法
            super().save_model(request, obj, form, change)

    # 禁用添加功能
    def has_add_permission(self, request):
        return False
