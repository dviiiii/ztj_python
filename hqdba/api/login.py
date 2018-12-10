from ..model.model_user import User
import hqdba.db.mysql as db_mysql

def queryPassword(pw):
    a = db_mysql.query("select * from hqdba_user")

    return a