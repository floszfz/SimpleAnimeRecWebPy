from django.db import models


# 评分模型类
class Rate(models.Model):
    id = models.AutoField(primary_key=True, db_column="rate_id", verbose_name='主键')
    # userid：用户模型对象；models.CASCADE：级联删除，当删除一个用户时，会同时删除这个用户下的所有评分
    userid = models.ForeignKey("app_user.User", models.CASCADE, db_column='rate_userid', blank=False, null=False,
                               verbose_name='用户名')
    # animeid：动漫模型对象；models.CASCADE：级联删除，当删除一个动漫时，会同时删除这个动漫下的所有评分
    animeid = models.ForeignKey("app_anime.Anime", models.CASCADE, db_column='rate_animeid', blank=False, null=False,
                                verbose_name='动漫名称')
    score = models.IntegerField(blank=False, null=False, db_column="rate_score", verbose_name='评分值')
    addtime = models.CharField(max_length=19, blank=False, null=False, db_column="rate_addtime", verbose_name='评分时间')

    # 嵌套类，给上级类添加功能或设置固定值
    class Meta:
        # 默认：True，当运行migrate或migrations命令时，当前数据库表会根据当前模型类更新；
        # 如果是False，则数据库表不会发生变化。
        managed = False
        db_table = 'db_rate'  # 模型类对应的数据库表
        verbose_name = "评分"  # 模型类名称
        verbose_name_plural = verbose_name  # 模型类复数名称
