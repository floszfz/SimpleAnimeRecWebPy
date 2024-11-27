from django.db import models


# 动漫类型模型类
class Type(models.Model):
    id = models.AutoField(primary_key=True, db_column="type_id", verbose_name='主键')
    typename = models.CharField(max_length=30, blank=False, null=False, db_column="type_typename",
                                verbose_name='动漫类型名称')

    # 将模型类以字符串的方式输出。在后台管理员添加、修改、删除等操作时显示返回的字符串，而不是模型类对象
    def __str__(self):
        return self.typename

    # 嵌套类，给上级类添加功能或设置固定值
    class Meta:
        # 默认：True，当运行migrate或migrations命令时，当前数据库表会根据当前模型类更新；
        # 如果是False，则数据库表不会发生变化。
        managed = False
        db_table = 'db_type'  # 模型类对应的数据库表
        verbose_name = "动漫类型"  # 模型类名称
        verbose_name_plural = verbose_name  # 模型类复数名称
