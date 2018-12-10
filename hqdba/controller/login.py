from django.shortcuts import render
import json
import hqdba.api.login as loginApi

from django.http import HttpResponse
from ..model.model_user import User


def index(request):
    key = "ztj_"
    json_result = json.loads( request.body )
    userName = json_result["userName"]
    password = json_result["password"]

    dbPassword = loginApi.queryPassword(userName)

    return HttpResponse( dbPassword )