from django.shortcuts import render
import json
import hqdba.api.login as loginApi
import hashlib

from django.http import HttpResponse


def index(request):
    key = "ztj_"
    json_result = json.loads( request.body )
    print(json_result)
    userName = json_result["userName"]
    password = json_result["password"]

    u_pass = hashlib.md5((password+key).encode("UTF8")).hexdigest()

    dbPassword = loginApi.queryPassword(userName)
    if u_pass == dbPassword[0]["user_password"]:
        m = 0

    else:
        m = 1

    return HttpResponse( [{'data': m}] )

def userinfo(request):
    key = "ztj_"
    json_result = json.loads( request.body )
    print(json_result)
    userName = json_result["userName"]
    password = json_result["password"]

    dbPassword = loginApi.queryPassword(userName)

    return HttpResponse( dbPassword )