# 项目主配置文件
# 项目启动从manage.py开始，manage.py会先加载settings.py中的配置信息
# setting.py中可以定义全局变量，变量名大写
import os
from pathlib import Path
from psutil import net_if_addrs
import time
import hashlib

# 项目根路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 加密盐或者秘钥，创建项目时由django框架随机生成该字符串。加密盐的作用是加密。
# 常用加密算法是MD5、hash等，加密原理是将字符串加密后的值保存在数据库、内存、文件中等。
# 比如：将管理员密码加密后保存在数据库中，但是如果管理员密码相对简单或者常见，那么很容易破解（加密算法加密后的值是固定的），
# 所以需要用到加密盐，常见用法是在加密算法加密后的值的前、中、后加上加密盐，或者其他一些操作。
# django默认使用的是哈希加密算法。
# django项目中：
# 1、防止CSRF跨站请求伪造攻击；2、建立会话时用到的sessionid；3、管理员密码
# 等情况都会用到加密算法
SECRET_KEY = 'on*=mmrs^x44mda&dz4c#c1#(mu&xv^98&3l&!0a2txphn3+6c'

# 开发模式，默认值是True。
# 在本地开发测试环境下设置True可以显示bug信息，便于找出代码bug所在位置。
# 当项目部署在服务器生产环境时，需要设置为False，因为debug模式下，项目异常后会在浏览器中提示很多异常信息和敏感数据信息。
DEBUG = True

# 设置能够访问本项目的ip地址，默认空列表。
# 当DEBUG = False时，必须填写。
# 有以下三种配置方法：
# 1、[]空列表：只有127.0.0.1或者localhost地址能访问本项目，即只有本机能够访问；
# 2、['*']：任何ip地址都可访问本项目；
# 3、['192.168.1.1', '192.168.1.2']：只有当前两个ip地址能访问本项目。
ALLOWED_HOSTS = ['*']

# 配置项目应用程序
# 创建项目时django框架会自动配置以django开头的默认应用程序。
# 每个应用程序都是一个可以独立运行的模块，通过将应用程序添加到INSTALLED_APPS设置中，
# django会在项目启动时自动加载并激活这些应用程序。
INSTALLED_APPS = [
    'simpleui',  # 使用django框架提供的后台管理员页面样式：django-simpleui
    # django默认组件：站点管理
    # django可以自动生成后台管理员的html页面，同时根据配置的自定义应用程序中的admin.py，将数据呈现在网页中实现数据的增删改查操作。
    # 'django.contrib.admin',
    # 重写django的默认站点管理：django.contrib.admin，主要是修改后台管理员菜单排序规则
    'utils.admin_site_util.AppAdminConfig',
    # django默认组件：权限管理
    # 结合数据库中以auth_开头的表实现后台管理员的权限管理功能，最终实现哪些管理员可以有哪些数据库数据的增删改查操作权限。
    'django.contrib.auth',
    # django默认组件：内容类型
    # 结合数据库表django_content_type实现model模型类与对应应用程序app的关联，
    # 同时为model模型（models.py中的实体类）提供数据库表的增删改查操作方法
    'django.contrib.contenttypes',
    # django默认组件：session会话
    # 结合数据库表django_session实现保存用户和管理员会话信息（包括登录信息，登录后，再次打开浏览器，那么已处于登录状态）
    'django.contrib.sessions',
    # django默认组件：消息管理
    # 用户后台管理员进行增删改查操作时成功、失败等的提示信息
    'django.contrib.messages',
    # django默认组件：静态文件管理
    # 静态文件指css、js等文件，该组件便于在html页面中加载静态文件
    'django.contrib.staticfiles',
    'app_index.apps.AppsConfig',  # 自定义组件：前台用户首页管理
    'app_public.apps.AppsConfig',  # 自定义组件：前台用户公共功能
    'app_anime.apps.AppsConfig',  # 自定义组件：动漫管理
    'app_type.apps.AppsConfig',  # 自定义组件：动漫类型管理
    'app_user.apps.AppsConfig',  # 自定义组件：用户管理
    'app_rate.apps.AppsConfig',  # 自定义组件：评分管理
    'app_analysis.apps.AppsConfig',  # 自定义组件：后台管理员数据分析管理
]

# django-simpleui配置
# 隐藏后台管理员首页链接
SIMPLEUI_HOME_INFO = False
# 隐藏后台管理员首页使用分析
SIMPLEUI_ANALYSIS = False
# 隐藏后台管理员首页最近动作
SIMPLEUI_HOME_ACTION = False
# 离线模式，加载本地的后台管理员css、js等静态资源
SIMPLEUI_STATIC_OFFLINE = True
# 指定simpleui默认的主题，一个样式文件名，文件相对路径从simpleui的theme目录读取
# 样式文件路径：Lib\site-packages\simpleui\static\admin\simpleui-x\theme
# 也可从后台管理员首页改变主题
SIMPLEUI_DEFAULT_THEME = 'e-blue.css'
# 修改默认后台管理员菜单图标，使用fontawesome图标
# 可到官网选择图标：https://fontawesome.com.cn/v5
SIMPLEUI_ICON = {
    '动漫类型管理': 'fa fa-list-ul',
    '动漫类型': 'fa fa-list-ul',
    '评分管理': 'fa fa-star',
    '评分': 'fa fa-star',
    '管理员': 'fa fa-user-cog',
}

# 配置项目中间件
# 中间件指用户在浏览器中操作向系统发出请求到用户得到请求结果，这个期间系统所做的操作。
# 用户的请求会从上到下依次执行MIDDLEWARE中的配置，然后服务器响应用户的时候会再次从下至上依次执行，
# 即在request请求前后和response响应前后执行。
# 执行过程：request-中间件-view-中间件-response-结束
MIDDLEWARE = [
    # django默认中间件：安全中间件
    # 为网站提供安全保护功能，比如设置xss防御的请求头，http协议转https协议等。
    'django.middleware.security.SecurityMiddleware',
    # django默认中间件：session会话中间件
    # 利用cookie在每个请求之间维护session会话状态，同时会给request添加一个处理好的session对象。
    'django.contrib.sessions.middleware.SessionMiddleware',
    # django默认中间件：通用中间件
    # 会处理一些用户请求的url地址，在url地址最后加反斜杠等。
    'django.middleware.common.CommonMiddleware',
    # django默认中间件：CSRF防御中间件
    # CSRF(cross site request forgery)是指跨站请求伪造，跨站请求伪造的问题在于，服务器信任来自客户端的数据，
    # 通过盗取会话的cookie信息，进而获取或者修改用户信息。
    # 该中间件增加防御保护以防止跨站伪造请攻击。通过向表单post请求中添加隐藏表单字段以及对请求进行检查以获取正确的值。
    'django.middleware.csrf.CsrfViewMiddleware',
    # django默认中间件：认证中间件
    # 该中间件会将当前登录的管理员信息添加到request对象中。
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # django默认中间件：消息中间件
    # 该中间件将处理系统和浏览器之间的所有临时消息。
    'django.contrib.messages.middleware.MessageMiddleware',
    # django默认中间件：点击劫持保护中间件
    # 该中间件确保项目的网页没有被嵌到别人的网站中去，从而避免了点击劫持 (clickjacking) 的攻击。
    # 通过在网页头部信息中增加X-Frame-OptionsLAI实现。
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件：前台用户权限验证中间件
    'utils.user_auth_util.UserAuthMiddleware',
]

# 设置允许同域名网站使用iframe打开页面
X_FRAME_OPTIONS = 'SAMEORIGIN'

# 设置主路由配置文件
ROOT_URLCONF = 'SimpleAnimeRecWebPy.urls'

# 设置模板配置信息，即html页面
TEMPLATES = [
    {
        # 模板渲染引擎，默认使用django提供的模板渲染，也可以使用jinja2模板渲染引擎
        # 模板渲染引擎的作用是将views.py视图函数中返回到页面的数据动态显示在页面中
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 模板文件所在位置，即html页面所在的文件夹
        'DIRS': [os.path.join(BASE_DIR, 'htmls')],
        # 是否允许在自定义应用程序包中查找模板文件
        'APP_DIRS': True,
        # 传递给模板引擎的其他参数，可以在html页面中直接使用
        'OPTIONS': {
            # django默认上下文处理器可以在模板中直接使用debug、request、auth、message等变量
            'context_processors': [
                # 在模板里面可以直接使用settings的DEBUG参数以及强大的sql_queries：它本身是一个字典，
                # 其中包括当前页面执行SQL查询所需的时间
                'django.template.context_processors.debug',
                # 在模板中可以直接使用request对象
                'django.template.context_processors.request',
                # 在模板里面可以直接使用user，perms对象
                'django.contrib.auth.context_processors.auth',
                # 在模板里面可以直接使用message对象
                'django.contrib.messages.context_processors.messages',
                # 可以在模板里面可以直接使用settings.py的MEDIA_URL变量
                'django.template.context_processors.media',
                # 还可以继续添加自定义配置
            ],
        },
    },
]

# WSGI即Web Server Gateway Interface，Web服务器网关接口，
# 是为Python语言定义的Web服务器和Web应用程序或框架之间的一种简单而通用的接口，用于django项目在服务器上的部署和上线。
# django3.0及以上版本推出了ASGI，ASGI即Asynchronous Server Gateway Interface，对应asgi.py文件，
# 简单理解：WSGI是同步、ASGI是异步，创建django项目时，会同时生成wsgi.py和asgi.py文件，并默认使用WSGI。
# 故此项目使用了wsgi.py，并未使用asgi.py。
# 配置WSGI文件位置
WSGI_APPLICATION = 'SimpleAnimeRecWebPy.wsgi.application'

# 配置数据库
# django目前支持sqlite、mysql、postgreSQL、oracle数据库
# sqlite数据库驱动：'django.db.backends.sqlite3',
# mysql数据库驱动：'django.db.backends.mysql'
# postgreSQL数据库驱动：'django.db.backends.postgresql_psycopg2',
# oracle数据库驱动：'django.db.backends.oracle'。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库驱动
        'NAME': 'simpleanimerecwebpy',  # 数据库名
        'USER': 'root',  # 数据库链接用户名
        'PASSWORD': 'root',  # 数据库链接密码
        'HOST': '127.0.0.1',  # 数据库链接地址
        'PORT': '3306',  # 数据库链接端口号
    }
}

# 后台管理员密码校验规则，django默认配置
AUTH_PASSWORD_VALIDATORS = [
    {  # 校验密码和管理员某些属性的相似性
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {  # 校验密码的最小长度(默认8)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {  # 校验密码是否出现在常用密码表中
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {  # 校验密码是否全为数字
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 设置语言为中文：zh-hans，默认英文：en-us
LANGUAGE_CODE = 'zh-hans'

# 设置时区Asia/Shanghai，UTC
TIME_ZONE = 'Asia/Shanghai'

# 设置国际化
USE_I18N = True

# 相同内容被不同时区地区的用户访问时，是否以不同格式内容展示（例如时间、日期、数字等）
USE_L10N = True

# 设置保存到数据库时间类型是否为UTC时间，如果不需要设置为false，默认为true
USE_TZ = False

# 设置静态资源文件访问url，静态资源包括css、js等
STATIC_URL = '/static/'

# 设置静态资源文件的存放位置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 设置上传文件访问url，上传文件包括用户头像、动漫图片等
MEDIA_URL = "/uploads/"

# 设置上传文件的存放位置
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads/")

# 日志配置
LOGGING = {
    'version': 1,  # 设置版本
    'disable_existing_loggers': False,  # 禁用默认配置中的所有记录器，采用自定义配置
    'handlers': {  # 日志处理器
        'console': {  # 控制台日志处理器
            'level': 'DEBUG',  # 日志级别：DEBUG
            'class': 'logging.StreamHandler',  # 日志处理器类
        },
        'file': {  # 文件日志处理器
            'level': 'DEBUG',  # 日志级别：DEBUG
            'class': 'logging.handlers.RotatingFileHandler',  # 日志处理器类
            'filename': 'D:/SimpleAnimeRecWebPy.log',  # 日志保存位置
            'maxBytes': 10 * 1024 * 1024,  # 日志文件最大大小：10MB
        },
    },
    'loggers': {  # 日志记录器
        # django内置日志记录器，记录数据库sql语句。
        # 其他django内置日志记录器：django、django.request、django.server、django.template。
        'django.db.backends': {
            'handlers': ['console'],  # 日志处理器，控制台
            'propagate': True,  # 允许传播至上级记录器
            'level': 'DEBUG',  # 日志级别：DEBUG
        },
        # django内置日志记录器，记录项目运行信息。
        # 其他django内置日志记录器：django.request、django.server、django.template、django.db.backends。
        'django': {
            'handlers': ['file'],  # 日志处理器，文件
            'propagate': True,  # 允许传播至上级记录器
            'level': 'DEBUG',  # 日志级别：DEBUG
        },
    }
}
