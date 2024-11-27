from app_user.models import User


# 数据分析模型类（不与数据库表绑定）
# 该类没有像其他模型类一样继承models.Model类，因为该类不需要与数据库表映射。
# 继承User模型类
class Analysis(User):
    # 嵌套类，给上级类添加功能或设置固定值
    class Meta:
        proxy = True  # 设置代理，可不与数据库表绑定
        verbose_name = "数据分析"  # 模型类名称
        verbose_name_plural = verbose_name  # 模型类复数名称
