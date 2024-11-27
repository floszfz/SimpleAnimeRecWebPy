# 前台用户权限验证中间件
# 该中间件会在执行具体的views视图函数之前执行，前台用户或者后台管理员的操作都会先执行该中间件，
# 其中管理员的权限验证这里不做处理，因为我们在settings.py中已经配置了django自带的管理员权限验证中间件：
# django.contrib.auth.middleware.AuthenticationMiddleware。
# 故该中间件只处理前台用户的权限验证。
# 权限验证是指：部分功能需要前台用户登录后才有操作权限，如果没有登录跳转到登录页面或者给用户提示需要先登录
from django.http import HttpResponseRedirect, HttpResponse
from SimpleAnimeRecWebPy import settings
from utils.utils import Constant
from django.utils.deprecation import MiddlewareMixin


# 创建前台用户权限验证中间件类
class UserAuthMiddleware(MiddlewareMixin):

    # 在执行具体的请求之前，进行验证
    def process_request(self, request):
        path = request.path  # 用户请求url地址
        # 设置前台用户不需要登录就可以访问的url地址，以逗号分割
        unAuthPath = ",/,/index,/login,/doLogin,/register,/doRegister,/logout," \
                     "/forgetPassword,/doForgetPassword,/anime/lists,/anime/detail,"
        # 如果请求地址是上传的资源文件或者后台管理员操作请求，不做处理
        if path.startswith(settings.MEDIA_URL) or path.startswith("/admin"):
            pass
        else:  # 前台用户的请求
            # 在请求的url地址前后加逗号
            path = "," + path + ","
            # 判断请求的url是否需要先登录
            if path not in unAuthPath:  # 需要登录
                # 判断session会话中是否有前台用户登录信息
                if request.session.get(Constant.session_user, None) is None:
                    # 用户的请求一般有两种：同步和异步，
                    # 同步：用户在页面点击一个链接直接跳转到另一个页面，比如：搜索功能，
                    # 异步：用户在页面点击按钮或者链接，网页通过javascript利用ajax异步提交数据到程序中，比如：评分功能。
                    # 同步操作，如果没有操作权限会直接跳转到登录页面，
                    # 异步操作，如果没有操作权限会返回没有操作权限的信息到网页中，网页中的javascript可以给用户提示信息。
                    # 判断是否是ajax异步请求
                    if request.headers.get('x-requested-with') and \
                            request.headers.get('x-requested-with').lower() == 'XMLHttpRequest'.lower():
                        # ajax异步请求
                        # 设置响应状态码403禁止访问，即：用户未登录，禁止操作
                        return HttpResponse(status=403)
                    else:
                        # 前台用户没有登录，跳转到前台登录页面
                        return HttpResponseRedirect('/login')  # 返回登录页面
