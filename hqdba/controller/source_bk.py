from django.shortcuts import render
import json
import hqdba.api.login as loginApi
import pymysql
import os
import paramiko



from django.http import HttpResponse


def source_bk_test(request):
    database_restore()
    return HttpResponse(11)



def get_user_info():
    """
    获取用户信息
    :return: 返回用户信息

    _db_name = input("Please enter the name of the database:")
    _user_name = input("Please enter the name of the user name:")
    _pwd = input("Please enter the name of the password:")
    _file_path = input("Please enter the database file path that needs to be restored and the name of the file:")
    """
    return 'ztj_db', 'root', 'Zudwa_2019', '/home/bk/ztj_db.sql'

def database_restore():
    """
    数据库还原
    :param _db_name: 数据库名称
    :param _user_name: 管理员username
    :param _pwd: 管理员密码
    :param _file_path: 还原的bak文件路径
    """

    try:
        # 获取用户信息
        _db_name, _user_name, _pwd, _file_path = get_user_info()
        # 判断文件是否存在
        file_exists = True

        """
        if not os.path.exists(_file_path):
            print("%s not find!" % _file_path)
            file_exists = False
        if file_exists:
            if _file_path[-4:] != ".bak":
                print("Unable to find the '.bak' file that needs to be restored!")
                file_exists = False
        """

        if file_exists:
            _host = "47.111.120.34"
            _port = 3306
            # 数据库连接参数
            conn = pymysql.connect('47.111.120.34', 'root', 'Zudwa_2019', 'ztj_db')
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            bk_path = '/home/bk/ztj_db.sql'
            try:
                # 执行sql语句
                cursor.execute('CREATE DATABASE IF NOT EXISTS ztj_db_test')
                results = cursor.fetchall()
                # 提交到数据库执行
                conn.commit()
            except:
                # Rollback in case there is any error
                conn.rollback()
            conn.close()


            ssh = paramiko.SSHClient()
            key = paramiko.AutoAddPolicy()
            ssh.set_missing_host_key_policy(key)
            ssh.connect('47.111.120.34', 22, 'root', 'Sau13407933414a', timeout=5)
            stdin, stdout, stderr = ssh.exec_command('mysql -uroot -pZudwa_2019  ztj_db_test  < /home/bk/ztj_db.sql')

            for i in stdout.readlines():
                print(i)



    except:
        print("Connected Failed,Please check whether the database information is correct!")


