import hqdba.db.mysql as db_mysql

def addConfig(params):
    result = db_mysql.insert_data("hqdba_db_config", params)
    return result

def queryConfig():
    result = db_mysql.query("select * from hqdba_db_config")
    return result