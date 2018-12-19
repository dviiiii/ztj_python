import hqdba.config.mysql_config as mysql_config
import pymysql
import hqdba.db.MysqlDb as Mysql
import hqdba.db.OracleDb as OracleDb
import cx_Oracle as oracle
# 打开数据库连接
default_config = mysql_config.default_config()

class Db(object):

    def __init__(self, config = default_config):
        if config["db_type"] == 'mysql':
            self.strategy = Mysql.MysqlDb(config)
        elif config["db_type"] == 'oracle':
            print('%s/%s@%s:%s/%s' % (
            config["db_user"], config["db_password"], config["db_host"], config["db_port"], config["db_name"]))
            self.strategy = OracleDb.OracleDb(config)


        elif config["db_type"] == 'sqlserver':
            print('sqlserver')
        else:
            print("other")
