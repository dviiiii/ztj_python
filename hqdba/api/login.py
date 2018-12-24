import hqdba.db.Db as db

def queryPassword(pw):
    DB = db.Db().strategy
    a = DB.executeSql("select * from hqdba_user")
    DB.close()
    return a