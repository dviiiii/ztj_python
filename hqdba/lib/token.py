import time, datetime
import jwt #pyjwt模块
from hqdba.config.config import config

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
                生成认证Token
                :param user_id: int
                :param login_time: int(timestamp)
                :return: string
                """
        try:
            """payload 中一些固定参数名称的意义, 同时可以在payload中自定义参数"""
            # iss  【issuer】发布者的url地址
            # sub 【subject】该JWT所面向的用户，用于处理特定应用，不是常用的字段
            # aud 【audience】接受者的url地址
            # exp 【expiration】 该jwt销毁的时间；unix时间戳
            # nbf  【not before】 该jwt的使用时间不能早于该时间；unix时间戳
            # iat   【issued at】 该jwt的发布时间；unix 时间戳
            # jti    【JWT ID】 该jwt的唯一ID编号
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config['SECRET_KEY'], options={'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


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