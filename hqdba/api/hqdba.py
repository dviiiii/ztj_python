import hqdba.db.Db as db
import hqdba.lib.Masking as ms

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
    result = DB.executeSql("select * FROM " + tableName + " limit 1,50")
    return result

def toMasking(config, json_result):
    DB = db.Db(config)
    tableName = json_result["tableName"]
    tableCol = json_result["tableCol"]
    masking_type = json_result["masking_type"]
    masking_other = json_result["masking_other"]
    print(json_result)
    result = []
    if masking_type == "getFixedValue":
        result = DB.executeSql("update " + tableName + " set " + tableCol + " = '"  + masking_other+"'")
    else:
        result = masking_tosql(config, json_result)
    return result

def masking_tosql(config, json_result):
    DB = db.Db( config )
    Masking = ms.Masking()
    tableName = json_result["tableName"]
    tableCol = json_result["tableCol"]
    masking_key = json_result["masking_key"]
    masking_type = json_result["masking_type"]
    masking_other = json_result["masking_other"]
    if not masking_other:
        masking_other = []
    result = DB.executeSql("select %s from %s" % (masking_key,tableName))

    whenstr = ""
    instr = ""
    for i in result:
        new_value = getattr(Masking, masking_type)(masking_other)
        whenstr += "WHEN %s THEN '%s' " % (str(i[masking_key]), new_value)
        instr += str(i[masking_key]) + ","

    DB.executeSql( "update %s set %s = CASE %s %s END where id in (%s)" % (tableName, tableCol, masking_key,whenstr, instr[0:-1]) )

    DB.close()
    return result