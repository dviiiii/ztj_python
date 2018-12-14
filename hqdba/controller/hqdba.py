import json
import hqdba.api.hqdba as hqdbaApi
import hqdba.lib.Masking as Masking

from django.http import JsonResponse


def test(request):
    mask = Masking.Masking()
    phone_num = mask.get_phone_num()
    randomNumber = mask.getRandomNumber(18,100,1)
    enum = mask.getEnum(['a', 'b', 'c'])
    name = mask.getName()
    gennerator = mask.getGennerator()
    email = mask.getEmail()

    for i in range(1):
        result = {
            "phone_num": mask.get_phone_num(),
            "randomNumber": mask.getRandomNumber( 1000, 10000, 2 ),
            "enum": mask.getEnum( ['男', '女', '人妖'] ),
            "name": mask.getName(),
            "gennerator": mask.getGennerator(),
            "email": mask.getEmail(),
        }
        status = hqdbaApi.addTest( result )
        print(i)

    return JsonResponse({"msg":0})

def addConfig(request):
    print( request.body )
    json_result = json.loads( request.body )

    status = hqdbaApi.addConfig(json_result)

    return JsonResponse( {"msg": status} )

def queryConfig(request):
    # json_result = json.loads( request.body )
    data = {}
    result = hqdbaApi.queryConfig()
    data["list"] = result

    return JsonResponse( data )

# 查询选择的实例中所有的表
def queryAllTables(request):
    json_result = json.loads( request.body )
    id = str(json_result["id"])
    global config_temp
    config_temp = hqdbaApi.queryConfig(id)[0]

    data = {}
    tbs = hqdbaApi.queryAllTables(config_temp)
    result = []
    for i in tbs:
        result.extend(i.values())
    data["list"] = result

    return JsonResponse( data )

# 根据表名查询表字段
def queryOneTableCol(request):
    json_result = json.loads( request.body )
    tableName = json_result["tableName"]
    data = {}
    global config_temp
    tbs = hqdbaApi.queryOneTableCol(config_temp, tableName)
    data["list"] = tbs

    return JsonResponse( data )

# 根据表名查询表字段
def queryOneTable(request):
    json_result = json.loads( request.body )
    tableName = json_result["tableName"]
    data = {}
    global config_temp
    tbs = hqdbaApi.queryOneTable(config_temp, tableName)
    data["list"] = tbs

    return JsonResponse( data )