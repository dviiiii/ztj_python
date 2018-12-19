import cx_Oracle


class OracleDb(object):

    def __init__(self, config):
        try:
            dsnStr= cx_Oracle.makedsn(config["db_host"], config["db_port"], config["db_name"])
            self.conn = cx_Oracle.connect(user=config["db_user"], password=config["db_password"], dsn=dsnStr)
        except:
            self.conn = cx_Oracle.connect('%s/%s@%s:%s/%s' %(config["db_user"], config["db_password"],config["db_host"],config["db_port"],config["db_name"]))
        self.cursor = self.conn.cursor()

    def executeSql(self, sql):
        print(sql)
        db = self.conn
        # 使用cursor()方法获取操作游标 pymysql.cursors.DictCursor
        cursor = self.cursor
        results = []
        # SQL 插入语句

        try:
            # 执行sql语句
            cursor.execute(sql)
            db.commit()
            index = cursor.description
            try:
                if index == None:
                    results = []
                else:
                    for res in cursor.fetchall():
                        print(res)
                        row = {}
                        for i in range(len(index)):
                            row[index[i][0]] = res[i]
                        results.append(row)
            except:
                results=[]

            # results = cursor.fetchall()


        except:
            # Rollback in case there is any error
            db.rollback()
        print(results)
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
        cursor = self.cursor
        cursor.close()
        db.close()

    def queryAllTables(self):
        print(1)
        return self.executeSql("select TNAME from TAB")

    def queryOneTableCol(self,tableName):
        data = self.executeSql("select  COLUMN_NAME  from user_tab_columns where Table_Name= '%s'" % tableName)
        result = []
        for i in data:
            row = {}
            row["Field"] = i["COLUMN_NAME"]
            result.append(row)
        return result

    def queryOneTable(self,tableName):
        return self.executeSql(
        " select * from %s where rownum < 50 minus select * from %s where rownum < 0" % (tableName, tableName))
