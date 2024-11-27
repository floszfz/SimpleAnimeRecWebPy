# 配置使用pymysql模块进行数据库操作
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)  # 配置pymysql版本
# django默认使用MySQLdb模块进行数据库的操作，但是MySQLdb目前并不支持python3及以上版本
# 配置pymysql作为MySQLdb使用
pymysql.install_as_MySQLdb()
# python3及以上版本连接MySQL的方案有：oursql, PyMySQL, myconnpy等模块
