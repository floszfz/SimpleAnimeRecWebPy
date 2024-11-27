# 主路由配置文件
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from SimpleAnimeRecWebPy import settings

urlpatterns = [
    path('', include('app_public.urls')),  # 前台用户公共路由：登录、注册、退出登录、文件上传等
    path('', include('app_index.urls')),  # 前台用户首页路由
    path('user/', include('app_user.urls')),  # 前台用户路由
    path('anime/', include('app_anime.urls')),  # 前台用户动漫路由
    path('rate/', include('app_rate.urls')),  # 前台评分路由
    path('admin/', admin.site.urls)  # 后台管理员路由
]

# 添加上传文件访问路由：指定访问url地址和上传文件文件夹位置
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 后台管理员登录页面登录框标题及后台管理员页面顶部标题
admin.site.site_header = "动漫推荐系统 · 管理员"
# 后台管理员各个网页的title标题
admin.site.site_title = "动漫推荐系统 · 管理员"
# 后台管理员首页标题
admin.site.index_title = "首页"
