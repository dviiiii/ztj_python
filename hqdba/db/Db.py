import hqdba.config.mysql_config as mysql_config
import pymysql
import cx_Oracle as oracle
# 打开数据库连接
default_config = mysql_config.default_config()

class Db(object):

    def __init__(self, config = default_config):
        if config["db_type"] == 'mysql':
            self.conn = pymysql.connect(config["db_host"], config["db_user"], config["db_password"], config["db_name"])
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        elif config["db_type"] == 'oracle':
            print('%s/%s@%s:%s/%s' %(config["db_user"], config["db_password"],config["db_host"],config["db_port"],config["db_name"]))
            dsnStr= oracle.makedsn(config["db_host"], config["db_port"], config["db_name"])
            self.conn = oracle.connect(user=config["db_user"], password=config["db_password"], dsn=dsnStr)
            self.cursor = self.conn.cursor()
        elif config["db_type"] == 'sqlserver':
            print('sqlserver')
        else:
            self.conn = pymysql.connect(config["db_host"], config["db_user"], config["db_password"], config["db_name"])
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def executeSql(self, sql):
        db = self.conn
        print(sql)
        # 使用cursor()方法获取操作游标 pymysql.cursors.DictCursor
        cursor = self.cursor
        results = ""
        # SQL 插入语句
        try:
            # 执行sql语句
            cursor.execute(sql)
            # results = cursor.fetchall()
            results = cursor.fetchall()
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        return results

    def insert_data(self,dbName,data_dict):
        try:

            data_values = "(" + "%s," * (len(data_dict)) + ")"
            data_values = data_values.replace(',)', ')')

            dbField = data_dict.keys()
            dataTuple = tuple(data_dict.values())
            dbField = str(tuple(dbField)).replace("'",'')
            conn =  self.conn
            cursor = self.cursor
            sql = """ insert into %s %s values %s """ % (dbName,dbField,data_values)
            params = dataTuple
            cursor.execute(sql, params)
            conn.commit()
            return 0

        except Exception as e:
            print("********  插入失败    ********")
            print(e)
            return 1


    def close(self):

        # 关闭数据库连接
        db = self.conn
        db.close()

    def makedict(self, cursor):
        result = cursor.fetchall()
        cur_desc = cursor.description
        colum = {}
        # print(cur_desc.__len__())
        for i in range(cur_desc.__len__()):
            for n in range(result.__len__()):
                try:
                    rs = result[n][i]
                except Exception as e:
                    print(e)
            colum[cur_desc[i][0]] = rs
        return colum
