import json
import hqdba.api.book as bookApi
import time, datetime
from hqdba.controller.rank import Rank

from django.http import JsonResponse

from hqdba.lib.token import Auth


# 获取书籍列表
def getBookList(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']
    data = {}
    result = bookApi.queryBookList(user_name)
    data["list"] = result

    return JsonResponse(data)


# 获取复习信息
def getReviewInfo(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']
    data = {}
    r_date = review_date()
    result = bookApi.getReviewInfo(user_name, r_date)
    data["list"] = result

    return JsonResponse(data)


#增加书籍
def addBook(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    params = json.loads(request.body)
    print(user_name)
    bookIsRepeat = bookApi.bookIsRepeat(user_name, params["bookName"])
    if bookIsRepeat != 0:
        return JsonResponse({"status": 1, "msg": "书籍已存在！"})
    else:
        filed = {
            "user_name": user_name,
            "book_name": params["bookName"],
            "book_number": params["bookNumber"],
            "read_type": params["readType"]
        }
        result = bookApi.addBook(filed)
        msg = "书籍新增成功！" if result == 0 else "书籍新增失败！"
        return JsonResponse({"status": result, "msg": msg})


# 删除书籍
def deleteBook(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    json_result = json.loads(request.body)

    try:
        bookApi.deleteBook(json_result, user_name)
        status = '删除成功！'
    except:
        status = '删除失败！'

    return JsonResponse({"msg": status})


# 新增读书记录
def addReadInfo(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    json_result = json.loads(request.body)
    json_result['today'] = datetime.datetime.now().strftime('%Y-%m-%d');
    try:
        bookApi.addReadInfo(json_result, user_name)
        status = '新增成功！'

        Rank.addRank(user_name, json_result['reading_rank'])
        updateProgess(json_result)
    except:
        status = '新增失败！'

    return JsonResponse({"msg": status})


# 复习时间
def review_date():
    now_time = datetime.datetime.now()
    one_time = now_time + datetime.timedelta(days=-1)
    one_time_nyr = one_time.strftime('%Y-%m-%d')

    two_time = now_time + datetime.timedelta(days=-2)
    two_time_nyr = two_time.strftime('%Y-%m-%d')

    four_time = now_time + datetime.timedelta(days=-4)
    four_time_nyr = four_time.strftime('%Y-%m-%d')

    seven_time = now_time + datetime.timedelta(days=-7)
    seven_time_nyr = seven_time.strftime('%Y-%m-%d')

    fifteen_time = now_time + datetime.timedelta(days=-15)
    fifteen_time_nyr = fifteen_time.strftime('%Y-%m-%d')

    dateList = [one_time_nyr, two_time_nyr, four_time_nyr, seven_time_nyr, fifteen_time_nyr]
    return dateList

# 更新进度
def updateProgess(params):
    progess = getProgess(params)
    nowProgess = len(progess)
    maxProgess = params['pagenumber']
    result = nowProgess*100/maxProgess
    bookApi.updateProgess(params['bookid'], result)

    return True


def getProgessInfo(request):
    token = request.META['HTTP_X_ACCESS_TOKEN']
    json_result = Auth.decode_auth_token(token)
    user_name = json_result['data']['id']

    json_result = json.loads(request.body)
    arr = getProgess({'bookid': json_result['id']})

    return JsonResponse({"list": arr})
# 得到进度list
def getProgess(params):
    arr = []
    bookReadInfo = bookApi.queryBookReadingInfo(params['bookid'])
    for i in bookReadInfo:
        begin_page = i['begin_page']
        end_page = i['end_page']
        for num in range(begin_page, end_page + 1):
            if num not in arr:
                arr.append(num)

    return arr

# 确认已复习
def checkReview(request):
    try:
        token = request.META['HTTP_X_ACCESS_TOKEN']
        json_result = Auth.decode_auth_token(token)
        user_name = json_result['data']['id']

        json_result = json.loads(request.body)
        r_date = {
            '0': 1,
            '1': 2,
            '2': 4,
            '3': 7,
            '4': 15
        }
        num = json_result['num']
        fixnum = -r_date[num]
        now_time = datetime.datetime.now()
        fix_time = now_time + datetime.timedelta(days=fixnum)
        fixday = fix_time.strftime('%Y-%m-%d')

        bookApi.checkReview(fixday, json_result['id'])
        Rank.addRank(user_name, 10)
        status = 0
    except:
        status = 1

    return JsonResponse({"status": status})
