import hqdba.db.Db as db
import hqdba.lib.Masking as ms

def bookIsRepeat(username, bookname):
    DB = db.Db().strategy

    result = DB.executeSql("select id from ol_book_info where username = '%s' and bookname = '%s'" %(username, bookname))
    DB.close()
    return len(result)

def addBook(params):
    DB = db.Db().strategy
    result = DB.insert_data("ol_book_info", params)
    DB.close()
    return result

def queryBookList(user_name):
    DB = db.Db().strategy
    where_sql = ' where 1=1 '
    if user_name != None:
        where_sql = where_sql + ' and user_name = "' + user_name + '"'
    result = DB.executeSql("select * from ol_book_info" + where_sql)
    DB.close()
    return result

#查询表名
def queryAllTables(config):
    DB = db.Db(config).strategy
    result = DB.queryAllTables()
    DB.close()
    return result

#根据表名查询列名
def queryOneTableCol(config, tableName):
    DB = db.Db(config).strategy
    result = DB.queryOneTableCol(tableName)
    DB.close()
    return result

def queryOneTable(config, tableName):
    DB = db.Db(config).strategy
    result = DB.queryOneTable(tableName)
    DB.close()
    return result

def toMasking(config, json_result):
    DB = db.Db(config).strategy
    tableName = json_result["tableName"]
    tableCol = json_result["tableCol"]
    masking_type = json_result["masking_type"]
    masking_other = json_result["masking_other"]
    print(json_result)
    result = []
    if masking_type == "getFixedValue":
        result = DB.executeSql("update " + tableName + " set " + tableCol + " = '"  + masking_other[0]+"'")
    else:
        result = masking_tosql(config, json_result)
    DB.close()
    return result

def masking_tosql(config, json_result):
    DB = db.Db( config ).strategy
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
        id = (i[masking_key])
        print(type(id) == int)
        if type(id) != int:
            id = str(id)
        whenstr += "WHEN %s THEN '%s' " % (id, new_value)
        instr += str(id) + ","

    DB.executeSql( "update %s set %s = CASE %s %s END where %s in (%s)" % (tableName, tableCol, masking_key,whenstr,masking_key, instr[0:-1]) )
    # DB.executeSql( "update \"TEST_MOBILE\" set \"MOBILE_NUM\" = CASE \"ID\" WHEN 1 THEN '13888888888' END where \"ID\" in (1)" )
    # DB.executeSql( "update TEST_MOBILE set MOBILE_NUM = '13888888888'")
    DB.close()
    return result