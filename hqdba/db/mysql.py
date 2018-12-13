import pymysql
import hqdba.config.mysql_config as mysql_config

# 打开数据库连接
config = mysql_config.default_config()

def query(sql):
    db = pymysql.connect(config["HOST"], config["USER"], config["PASSWORD"], config["NAME"])

    # 使用cursor()方法获取操作游标 pymysql.cursors.DictCursor
    cursor = db.cursor(pymysql.cursors.DictCursor)
    results = ""
    # SQL 插入语句
    try:
       # 执行sql语句
       cursor.execute(sql)
       results = cursor.fetchall()
       print(results)
       # 提交到数据库执行
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

    # 关闭数据库连接
    db.close()
    return results

def insert_data(dbName,data_dict):

    try:

        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')

        dbField = data_dict.keys()
        dataTuple = tuple(data_dict.values())
        dbField = str(tuple(dbField)).replace("'",'')
        conn =  pymysql.connect(config["HOST"], config["USER"], config["PASSWORD"], config["NAME"])
        cursor = conn.cursor()
        sql = """ insert into %s %s values %s """ % (dbName,dbField,data_values)
        params = dataTuple
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()

        return 0

    except Exception as e:
        print("********  插入失败    ********")
        print(e)
        return 1