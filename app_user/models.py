from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from utils.utils import Utils


# 用户模型类
class User(models.Model):
    id = models.AutoField(primary_key=True, db_column="user_id", verbose_name='主键')
    # unique：唯一，用户名不能重复
    uname = models.CharField(max_length=30, blank=False, null=False, db_column="user_uname",
                             unique=True, verbose_name='用户名')
    password = models.CharField(max_length=30, blank=False, null=False, db_column="user_password", verbose_name='登录密码')
    fullname = models.CharField(max_length=30, blank=False, null=False, db_column="user_fullname", verbose_name='用户姓名')
    # upload_to：重置上传文件文件名
    headpic = models.ImageField(upload_to=Utils().resetUploadFileName, blank=False, null=False,
                                db_column="user_headpic", verbose_name="用户头像")
    # 用户性别，1：男，2：女
    gender = models.IntegerField(blank=False, null=False, choices=[(1, "男"), (2, "女")],
                                 db_column="user_gender", verbose_name='用户性别')
    # 用户年龄，范围10-90
    age = models.IntegerField(blank=False, null=False, db_column="user_age", verbose_name='用户年龄',
                              validators=[MaxValueValidator(90), MinValueValidator(10)])
    # validators：正则表达式验证电话格式
    phone = models.CharField(max_length=11, blank=False, null=False,
                             validators=[validators.RegexValidator("^1[3-9]\d{9}$", "电话格式不正确！")],
                             db_column="user_phone", verbose_name='用户电话')
    # validators：django提供验证邮箱格式
    mailbox = models.CharField(max_length=50, blank=False, null=False,
                               validators=[validators.EmailValidator(message="邮箱格式不正确！")],
                               db_column="user_mailbox", verbose_name='用户邮箱')
    introduction = models.TextField(max_length=1000, blank=False, null=False, db_column="user_introduction",
                                    verbose_name='个人简介')
    addtime = models.CharField(max_length=19, blank=False, null=False, db_column="user_addtime", verbose_name='注册时间')

    # 将模型类以字符串的方式输出。在后台管理员添加、修改、删除等操作时显示返回的字符串，而不是模型类对象
    def __str__(self):
        return self.uname

    # 用户模型对象转字典格式，用于用户登录后将用户信息保存在session会话中
    def convert_dict(self):
        return {
            "id": self.id,
            "uname": self.uname,
            "headpicname": self.headpic.name,
            "headpicurl": self.headpic.url
        }

    # 嵌套类，给上级类添加功能或设置固定值
    class Meta:
        # 默认：True，当运行migrate或migrations命令时，当前数据库表会根据当前模型类更新；
        # 如果是False，则数据库表不会发生变化。
        managed = False
        db_table = 'db_user'  # 模型类对应的数据库表
        verbose_name = "用户"  # 模型类名称
        verbose_name_plural = verbose_name  # 模型类复数名称
