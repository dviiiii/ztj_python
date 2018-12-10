import pymysql
import hqdba.config.mysql_config as mysql_config

# 打开数据库连接
config = mysql_config.default_config()

def query(sql):
    db = pymysql.connect(config["HOST"], config["USER"], config["PASSWORD"], config["NAME"])

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    results = ""
    # SQL 插入语句
    try:
       # 执行sql语句
       cursor.execute(sql)
       results = cursor.fetchall()
       # 提交到数据库执行
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

    # 关闭数据库连接
    db.close()
    return results