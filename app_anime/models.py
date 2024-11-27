from django.db import models
from utils.utils import Utils


# 动漫模型类
class Anime(models.Model):
    id = models.AutoField(primary_key=True, db_column="anime_id", verbose_name='主键')
    animename = models.CharField(max_length=100, blank=False, null=False, db_column="anime_animename",
                                 verbose_name='动漫名称')
    # typeid：动漫类型模型对象；models.CASCADE：级联删除，当删除一个动漫类型时，会同时删除这个动漫类型下的所有动漫
    typeid = models.ForeignKey('app_type.Type', models.CASCADE, db_column='anime_typeid',
                               blank=False, null=False, verbose_name='动漫类型')
    # upload_to：重置上传文件文件名
    pic = models.ImageField(upload_to=Utils().resetUploadFileName, blank=False, null=False,
                            db_column="anime_pic", verbose_name="动漫图片")
    introduction = models.TextField(max_length=2000, blank=False, null=False, db_column="anime_introduction",
                                    verbose_name='动漫简介')
    weburl = models.CharField(max_length=100, blank=False, null=False, db_column="anime_weburl",
                              verbose_name='B站动漫链接')
    addtime = models.CharField(max_length=19, blank=False, null=False, db_column="anime_addtime", verbose_name='添加时间')

    # 将模型类以字符串的方式输出。在后台管理员添加、修改、删除等操作时显示返回的字符串，而不是模型类对象
    def __str__(self):
        return self.animename

    # 嵌套类，给上级类添加功能或设置固定值
    class Meta:
        # 默认：True，当运行migrate或migrations命令时，当前数据库表会根据当前模型类更新；
        # 如果是False，则数据库表不会发生变化。
        managed = False
        db_table = 'db_anime'  # 模型类对应的数据库表
        verbose_name = "动漫"  # 模型类名称
        verbose_name_plural = verbose_name  # 模型类复数名称
