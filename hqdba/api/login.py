import hqdba.db.Db as db

def queryPassword(pw):
    DB = db.Db()
    a = DB.executeSql("select * from hqdba_user")

    return a