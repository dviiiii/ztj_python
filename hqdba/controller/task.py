import json

import time, datetime
from hqdba.controller.rank import Rank
from hqdba.api.task import Task

from django.http import JsonResponse

from hqdba.lib.token import Auth


# 新增任务
def addTask(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    params = json.loads(request.body)
    params['task_create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 0 == params['task_repeat_end']:
        params['task_repeat_end'] = '2100-01-01'
    print(params)
    data = {}
    result = Task.addTask(user_name, params)
    data["list"] = result

    return JsonResponse(data)


# 查询任务
def queryTask(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    params = json.loads(request.body)
    params['begin'] += ' 00:00:00'
    params['end'] += ' 23:59:59'
    print(params)
    data = {}
    result = Task.queryTask(user_name, params)
    data["list"] = result

    return JsonResponse(data)

# 完成任务
def completeTask(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    params = json.loads(request.body)
    print(params)
    params['complete_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = Task.completeTask(user_name, params)
    data = {}

    data["list"] = result
    print(data)

    return JsonResponse(data)
