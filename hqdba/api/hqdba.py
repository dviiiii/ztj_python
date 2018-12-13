import hqdba.db.mysql as db_mysql

def addTest(params):
    result = db_mysql.insert_data("hqdba_db_test", params)
    return result

def addConfig(params):
    result = db_mysql.insert_data("hqdba_db_config", params)
    return result

def queryConfig():
    result = db_mysql.query("select * from hqdba_db_config")
    return result