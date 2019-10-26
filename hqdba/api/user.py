import hqdba.db.Db as db

def queryPassword(username):
    DB = db.Db().strategy
    a = DB.executeSql("select user_password from system_user where user_name = '%s'" % username)
    DB.close()
    return a