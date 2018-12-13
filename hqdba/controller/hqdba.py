import json
import hqdba.api.hqdba as hqdbaApi

from django.http import JsonResponse


def addConfig(request):
    json_result = json.loads( request.body )
    status = hqdbaApi.addConfig(json_result)

    return JsonResponse( status )

def queryConfig(request):
    # json_result = json.loads( request.body )
    data = {}
    result = hqdbaApi.queryConfig()
    data["list"] = result

    return JsonResponse( data )