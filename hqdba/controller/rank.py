import hqdba.db.Db as db


class Rank:
    @staticmethod
    def addRank(user_name, rank_val):
        """
                增加积分
                :param rank_val: int
                :param user_name: str
                :return: dict
                """
        try:
            DB = db.Db().strategy
            sql = "UPDATE ol_user_info SET rank=rank + %s WHERE user_name = '%s' " % (rank_val, user_name)
            result = DB.executeSql(sql)
            DB.close()
            return result
        except Exception as e:
            return e

    @staticmethod
    def queryRank(user_name):
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

    # def identify(self, request):
    #     """
    #     用户鉴权
    #     :return: list
    #     """
    #     auth_header = request.headers.get('Authorization')
    #     if (auth_header):
    #         auth_tokenArr = auth_header.split(" ")
    #         if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
    #             result = common.falseReturn('', '请传递正确的验证头信息')
    #         else:
    #             auth_token = auth_tokenArr[1]
    #             payload = self.decode_auth_token(auth_token)
    #             if not isinstance(payload, str):
    #                 user = Users.get(Users, payload['data']['id'])
    #                 if (user is None):
    #                     result = common.falseReturn('', '找不到该用户信息')
    #                 else:
    #                     if (user.login_time == payload['data']['login_time']):
    #                         result = common.trueReturn(user.id, '请求成功')
    #                     else:
    #                         result = common.falseReturn('', 'Token已更改，请重新登录获取')
    #             else:
    #                 result = common.falseReturn('', payload)
    #     else:
    #         result = common.falseReturn('', '没有提供认证token')
    #     return result
