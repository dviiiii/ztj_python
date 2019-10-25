import hqdba.db.Db as db
import hqdba.lib.Masking as ms


# 查询书籍列表
def queryBookList(user_name):
    DB = db.Db().strategy
    where_sql = ' where 1=1 '
    if user_name is not None:
        where_sql = where_sql + ' and user_name = "' + user_name + '" and is_delete = 0'
    result = DB.executeSql("select * from ol_book_info" + where_sql)
    DB.close()
    return result


# 查询复习信息
def getReviewInfo(user_name, review_date):
    DB = db.Db().strategy
    where_sql = ' where 1=1 '
    if user_name is not None:
        where_sql = where_sql + ' and user_name = "' + user_name + '"'
        where_sql = """%s and a.user_name = '%s'
        and a.is_delete = '0' 
        and a.read_type='0'
        and (b.review_num = '0' and b.create_date <= '%s')
        or (b.review_num = '1' and b.create_date <= '%s')
        or (b.review_num = '2' and b.create_date <= '%s')
        or (b.review_num = '3' and b.create_date <= '%s')
        or (b.review_num = '4' and b.create_date <= '%s')
        """ % (where_sql, user_name, review_date[0], review_date[1], review_date[2], review_date[3], review_date[4])
    result = DB.executeSql("select b.id, a.book_name,b.begin_page,b.end_page,b.create_date,b.review_num from ol_book_info a LEFT JOIN ol_book_reading b ON a.id = b.book_id" + where_sql)
    DB.close()
    return result

def addBook(params):
    DB = db.Db().strategy
    result = DB.insert_data("ol_book_info", params)
    DB.close()
    return result


def bookIsRepeat(username, bookname):
    DB = db.Db().strategy

    result = DB.executeSql("select id from ol_book_info where user_name = '%s' and book_name = '%s' and is_delete = '0'" %(username, bookname))
    DB.close()
    return len(result)


# 删除书籍
def deleteBook(params, user_name):
    DB = db.Db().strategy
    book_id = params['id']
    result = DB.executeSql("update ol_book_info set is_delete=1 where id = %s and user_name = '%s' " % (book_id, user_name))
    DB.close()
    return result

def addReadInfo(params, user_name):
    DB = db.Db().strategy
    print(params)

    result = DB.executeSql("insert into ol_book_reading(book_id, begin_page, end_page,create_date) values(%s, %s, %s, %s)" % (params['bookid'], params['bookPageNumberS'], params['bookPageNumberE'], params['today']))
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