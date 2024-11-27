import os
import random
from django.db.models import Func
import datetime, time
from django.db import connection


# 公共常量类
class Constant(object):

    page_size_user = 10  # 前台用户端分页大小，即列表页面每页显示的数据数量

    page_size_admin = 10  # 后台管理员端分页大小，即列表页面每页显示的数据数量

    password_default_user = "123456"  # 前台用户忘记密码后的新密码和后台管理员重置用户密码后的新密码

    header_default_user = "user_pic.jpg"  # 默认用户头像

    session_user = "session_user"  # session会话中以键值对的形式保存登录用户信息，定义登录用户session中键的名称


# 常用工具类
class Utils(object):

    # 获取当前时间
    def getCurrentTime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 获取时间戳+六位随机数，用于上传文件重命名
    def getCurrentTimeRandom(self):
        strTemp = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            strTemp += ch
        return str(round(time.time() * 1000)) + "_" + strTemp

    # 重置上传文件文件名，上传的文件需要重命名，文件名唯一
    def resetUploadFileName(self, instance, filename):
        filetype = os.path.splitext(filename)[1]  # 获取文件名后缀，例如：.jpg
        filename = self.getCurrentTimeRandom() + filetype  # 产生一个随机文件名称：时间_随机数.文件格式
        return "{file}".format(file=filename)  # 返回新文件名

    # 整理分页显示
    # 将前台用户端分页显示为：1 2 3 4 5
    def arrangePageBean(self, pageBean, data):
        # 判断分页是否有数据
        if pageBean is not None and len(pageBean) > 0:
            showPagesParam = 9  # 定义变量，显示9个页面数字
            # 中间显示的页面数字
            showHalfPagesParam = (showPagesParam - 1) / 2
            # 从第几页开始展示
            beginPageNumParam = 1
            # 判断当前页面小于总页面数的一半减一，同时总页面数减去当前页面大于或者等于总页面数的一半减一
            if pageBean.number - showHalfPagesParam > 1 and pageBean.paginator.num_pages - pageBean.number >= showHalfPagesParam:
                # 开始页面是当前页面减去总页面数的一半减一
                beginPageNumParam = pageBean.number - showHalfPagesParam
            else:
                # 判断总页面数减去当前页面小于总页面数的一半减一，同时总页面数大于展示的页面总数
                if pageBean.paginator.num_pages - pageBean.number < showHalfPagesParam and pageBean.paginator.num_pages > showPagesParam:
                    # 开始页面是总页面数减去总页面数的一半加一
                    beginPageNumParam = pageBean.paginator.num_pages - showPagesParam + 1
                else:
                    beginPageNumParam = 1
            # 展示的尾页面数字
            endPageNumParam = pageBean.paginator.num_pages
            if pageBean.paginator.num_pages > showPagesParam:
                endPageNumParam = beginPageNumParam + showPagesParam - 1
            # 页面最终展示的分页起始页面数
            data["showPageRange"] = range(int(beginPageNumParam), int(endPageNumParam) + 1)
        return data


# 自定义原生sql语句查询工具类
# 有些功能的数据库操作需要使用自定义原生sql语句，该类主要是执行sql语句。
# 一般功能我们可以使用例如：model.save()、Model.objects.filter()等django内置数据库操作方法实现，
# 但是还有一些功能需要执行自定义原生sql语句，django也提供了执行自定义原生sql语句的方法：
# Model.objects.raw(sql)、Model.objects.extra()等，但是以上方法都有一些局限性。
# 故该方法使用django提供的connection执行sql语句，并返回字典格式数据
class SqlQueryUtils(object):

    # 查询所有数据，参数：params即查询参数
    def sql_query_all(self, sql, params=None):
        # 定义返回的结果
        query_data = list()
        # 查询，使用django框架提供的connection对象实现数据库查询
        with connection.cursor() as cursor:
            # 执行sql语句，返回的数据中，字段和数据是分开的，没有一一对应
            cursor.execute(sql, params)
            # 获取查询结果的字段名
            # description属性得到由字段和其他值组成的元组，格式：((字段1，...),(字段2，...)...)
            query_field_names = [k[0] for k in cursor.description]
            # 获取所有数据值，格式[(字段1的值,字段2的值....)，(字段1的值,字段2的值....)]，是一个由元组组成的列表
            query_field_values = cursor.fetchall()
            # 将字段名和字段值一一对应并转dict格式
            for query_field_value in query_field_values:
                result = dict(zip(query_field_names, query_field_value))
                query_data.append(result)
        return query_data


# 重写mysql数据库内置函数round()，对数据四舍五入并保留几位小数
# 在mysql中round(val, 1)函数，val：数值，1：保留一位小数，即将val四舍五入并保留一位小数输出，如果参数1没有，那么取整。
# 举例：Userscore.objects.values("userid").annotate(Avg("score"))，即分组查询每个用户的平均评分，
# 平均评分值是小数并默认保留四位小数，例如：3.3333（除不尽）或者5.0，但是我们想要的结果是3.3或者5.0。
# 可以如下操作：
# from django.db.models.functions import Round
# Userscore.objects.values("userid").annotate(Round(Avg("score")))
# django提供了Round()类，具体执行的sql语句：round(avg(score))，
# 但是因为没有约束保留的小数位数，所以结果都是整数并会四舍五入，也不是理想的效果。
# django4.0优化了Round()类，添加了保留小数位数的参数，但是django3.0不支持并将报错：
# Userscore.objects.values("userid").annotate(Round(Avg("score"), 1))
# 具体执行的sql语句：round(avg(score) ,1)，这是我们先要的结果。
# 因此为了同时兼容django3.0和django4.0，自定义Round()类。
class DBRoundUtils(Func):
    # mysql内置函数名称
    function = 'ROUND'
    # 函数内容，最终效果举例：round(avg(score) ,1)，即将 avg(score)的值四舍五入并保留一位小数输出
    template = '%(function)s(%(expressions)s, 1)'
