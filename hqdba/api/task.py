import hqdba.db.Db as db


class Task:
    @staticmethod
    def addTask(user_name, params):
        """
                增加任务
                :param params: object
                :param user_name: str
                :return: dict
                """
        try:
            DB = db.Db().strategy
            sql = """insert into 
                        ol_task(user_name, task_name, task_add_rank, task_reduce_rank, 
                        task_mark, task_create_time, task_plan_complete_time,
                        task_quadrant, task_repeat_type, task_repeat_point, task_repeat_end) 
                        values('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s' )""" \
                  % (user_name, params['task_name'], params['task_add_rank'], params['task_reduce_rank'],
                     params['task_mark'], params['task_create_time'], params['task_plan_complete_time'],
                     params['task_quadrant'], params['task_repeat_type'], params['task_repeat_point'], params['task_repeat_end'],
                     )
            print(sql)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e

    @staticmethod
    def queryTask(user_name, params):
        """
                查询积分
                :param user_name: str
                :return: dict
                """
        print(user_name)
        try:
            DB = db.Db().strategy
            wheresql = ' 1=1 '
            if params['task_status'] != '-1':
                wheresql += 'and task_status = ' + params['task_status']
            sql = "SELECT * from ol_task WHERE user_name = '%s' and task_create_time > '%s' and task_create_time < '%s' and is_delete = 0 and  %s" \
                  % (user_name, params['begin'], params['end'], wheresql)
            print(sql)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e

    @staticmethod
    def deleteTask(user_name, params):
        """
                查询积分
                :param user_name: str
                :return: dict
                """
        print(user_name)
        try:
            DB = db.Db().strategy
            sql = "SELECT rank from ol_user_info WHERE user_name = '%s' " % (user_name)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e

    @staticmethod
    def updateTask(user_name, params):
        """
                查询积分
                :param user_name: str
                :return: dict
                """
        print(user_name)
        try:
            DB = db.Db().strategy
            sql = "SELECT rank from ol_user_info WHERE user_name = '%s' " % (user_name)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e

    @staticmethod
    def completeTask(user_name, params):
        """
                完成任务
                :param user_name: str
                :return: dict
                """
        print(user_name)
        try:
            DB = db.Db().strategy
            sql = "UPDATE ol_task SET task_status='1' , task_complete_time='%s' where id='%s';" % (params['complete_time'], params['id'] )
            print(sql)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e
