import hqdba.db.Db as db

def addTest(params):
    DB = db.Db()
    result = DB.insert_data("hqdba_db_test", params)
    return result

def addConfig(params):
    DB = db.Db()
    result = DB.insert_data("hqdba_db_config", params)
    return result

def queryConfig(id = None):
    DB = db.Db()
    where_sql = ' where 1=1 '
    if id != None:
        where_sql = where_sql + ' and id = ' + id
    result = DB.executeSql("select * from hqdba_db_config" + where_sql)
    return result

def queryAllTables(config):
    DB = db.Db(config)
    result = DB.executeSql("show tables")
    return result

def queryOneTableCol(config, tableName):
    DB = db.Db(config)
    result = DB.executeSql("SHOW COLUMNS FROM " + tableName)
    return result

def queryOneTable(config, tableName):
    DB = db.Db(config)
    result = DB.executeSql("select * FROM " + tableName + " limit 1,5")
    print(result)
    return result