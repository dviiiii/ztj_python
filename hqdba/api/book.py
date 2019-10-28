import hqdba.db.Db as db
import hqdba.lib.Masking as ms


# 查询书籍列表
def queryBookList(user_name):
    DB = db.Db().strategy
    where_sql = ' where 1=1 '
    if user_name is not None:
        where_sql = where_sql + ' and user_name = "' + user_name + '" and is_delete = 0 and book_status != 100'
    print(where_sql)
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

# 新增书籍
def addBook(params):
    DB = db.Db().strategy
    result = DB.insert_data("ol_book_info", params)
    DB.close()
    return result

# 验证书籍是否重复
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

# 增加阅读记录
def addReadInfo(params, user_name):
    DB = db.Db().strategy
    sql = "insert into ol_book_reading(book_id, begin_page, end_page,create_date) values(%s, %s, %s, '%s')" % (params['bookid'], params['bookPageNumberS'], params['bookPageNumberE'], params['today'])
    print(sql)

    result = DB.executeSql(sql)
    DB.close()
    return result


#查询某本书的读书记录
def queryBookReadingInfo(book_id):
    DB = db.Db().strategy
    result = DB.executeSql("select begin_page,end_page from ol_book_reading where book_id = %s and is_delete=0" % book_id)
    DB.close()
    return result


# 更新读书进度
def updateProgess(book_id, pro):
    DB = db.Db().strategy
    result = DB.executeSql("update ol_book_info set book_status= %s where id= %s" % (pro, book_id))
    DB.close()
    return result

# 更新复习信息
def checkReview(fixday, book_id):
    DB = db.Db().strategy
    sql = "UPDATE ol_book_reading SET review_num = review_num+1,create_date='%s' WHERE id = %s" % (fixday, book_id)
    result = DB.executeSql(sql)
    DB.close()
    return result