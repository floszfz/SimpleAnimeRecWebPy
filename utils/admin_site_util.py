# 后台管理员配置，重写django默认配置，主要是修改后台管理员菜单排序规则
from django.contrib.admin.apps import AdminConfig
from django.contrib.admin import AdminSite


# 定义后台管理员配置类，继承自django框架默认后台管理员配置
class AppAdminConfig(AdminConfig):

    # 设置后台管理员站点配置类，默认是：django.contrib.admin.sites.AdminSite
    default_site = 'utils.admin_site_util.AppAdminSiteConfig'


# 定义后台管理员站点配置类，继承自django框架默认后台管理员站点配置类
class AppAdminSiteConfig(AdminSite):

    def __init__(self):
        # 重定义后台管理员菜单auth（认证和授权信息）下的二级菜单user显示用户，改为：管理员
        from django.contrib.auth.models import User
        User._meta.verbose_name_plural = "管理员"
        # 调用父类init方法
        super().__init__()

    # 重写后台管理员菜单排序规则
    def get_app_list(self, request, app_label=None):
        # 定义后台管理员菜单顺序字典
        new_menu_order_dict = {
            'app_analysis': 0,  # 数据分析
            'app_user': 1,  # 用户管理
            'app_anime': 10,  # 动漫管理
            'app_type': 20,  # 动漫类型管理
            'app_rate': 30,  # 评分管理
            'auth': 80,  # 认证和授权管理
        }
        # 获取后台管理员菜单字典
        app_dict = self._build_app_dict(request)
        # 原django排序代码，根据每个模块首字符升序排列：
        # app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # 重新排序，根据new_menu_order_dict字典的值升序排列
        app_list = sorted(app_dict.values(), key=lambda x: new_menu_order_dict[x['app_label']])
        # 原django排序代码，每个模块下的子模块排序，根据每个模块首字符升序排列
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list
