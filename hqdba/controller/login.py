from django.shortcuts import render
import json
import hqdba.api.login as loginApi
import hashlib
import time, datetime

from hqdba.lib.token import Auth

from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    key = "ztj_"
    json_result = json.loads( request.body )

    userName = json_result["userName"]
    password = json_result["password"]

    u_pass = hashlib.md5((password+key).encode("UTF8")).hexdigest()
    dbPassword = loginApi.queryPassword(userName)

    m = 1
    token = ''
    if dbPassword:
        if  u_pass == dbPassword[0]["user_password"]:
            m = 0
            token = Auth.encode_auth_token(userName, time.time()).decode()
        else:
            m = 1

    return JsonResponse( {'status': m, 'token': token} )

def userinfo(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    print(json_result)

    return JsonResponse( {'status': json_result} )