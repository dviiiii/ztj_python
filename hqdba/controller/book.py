import json
import hqdba.api.hqdba as hqdbaApi
import hqdba.api.book as bookApi


from django.http import JsonResponse

from hqdba.lib.token import Auth


def addBook(request):
    username = 'admin'
    params = json.loads(request.body)
    print(params)
    bookIsRepeat = bookApi.bookIsRepeat(username, params["bookName"])
    if bookIsRepeat !=0:
        return JsonResponse({"status": 1, "msg": "书籍已存在！"})
    else:
        filed = {
            "username": username,
            "bookname": params["bookName"],
            "booknumber": params["bookNumber"],
            "readtype": params["readType"]
        }
        result = bookApi.addBook(filed)
        msg = "书籍新增成功！" if result == 0 else "书籍新增失败！"
        return JsonResponse( {"status": result,"msg": msg} )



def addConfig(request):
    print( request.body )
    json_result = json.loads( request.body )

    status = hqdbaApi.addConfig(json_result)

    return JsonResponse( {"msg": status} )

def getBookList(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']
    data = {}
    result = bookApi.queryBookList(user_name)
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
    print(tbs)
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

# 根据表名查询表字段
def toMasking(request):
    json_result = json.loads( request.body )
    data = {}
    global config_temp
    tbs = hqdbaApi.toMasking(config_temp, json_result)
    data["list"] = tbs

    return JsonResponse( data )