import datetime

import hqdba.db.Db as db
import hqdba.lib.Masking as ms



def addTest(params):
    DB = db.Db().strategy
    result = DB.insert_data("hqdba_db_test", params)
    DB.close()
    return result

def addConfig(params):
    DB = db.Db().strategy
    result = DB.insert_data("hqdba_db_config", params)
    DB.close()
    return result

#查询数据库实例配置
def queryConfig(id = None):
    DB = db.Db().strategy
    where_sql = ' where 1=1 '
    if id != None:
        where_sql = where_sql + ' and id = ' + id
    result = DB.executeSql("select * from hqdba_db_config" + where_sql)
    DB.close()
    return result

#查询表名
def queryAllTables(config):
    DB = db.Db(config).strategy
    result = DB.queryAllTables()
    DB.close()
    return result

#根据表名查询列名
def queryOneTableCol(config, tableName):
    DB = db.Db(config).strategy
    result = DB.queryOneTableCol(tableName)
    DB.close()
    return result

def queryOneTable(config, tableName):
    DB = db.Db(config).strategy
    result = DB.queryOneTable(tableName)
    DB.close()
    return result

def toMasking(config, json_result):
    DB = db.Db(config).strategy
    tableName = json_result["tableName"]
    tableCol = json_result["tableCol"]
    masking_type = json_result["masking_type"]
    masking_other = json_result["masking_other"]
    print(json_result)
    result = []
    if masking_type == "getFixedValue":
        result = DB.executeSql("update " + tableName + " set " + tableCol + " = '"  + masking_other[0]+"'")
    else:
        result = masking_tosql(config, json_result)
    DB.close()
    return result

def masking_tosql(config, json_result):
    DB = db.Db( config ).strategy
    Masking = ms.Masking()
    tableName = json_result["tableName"]
    tableCol = json_result["tableCol"]
    masking_key = json_result["masking_key"]
    masking_type = json_result["masking_type"]
    masking_other = json_result["masking_other"]
    if not masking_other:
        masking_other = []
    result = DB.executeSql("select %s from %s" % (masking_key,tableName))

    whenstr = ""
    instr = ""
    for i in result:
        new_value = getattr(Masking, masking_type)(masking_other)
        id = (i[masking_key])
        print(type(id) == int)
        if type(id) != int:
            id = str(id)
        whenstr += "WHEN %s THEN '%s' " % (id, new_value)
        instr += str(id) + ","

    DB.executeSql( "update %s set %s = CASE %s %s END where %s in (%s)" % (tableName, tableCol, masking_key,whenstr,masking_key, instr[0:-1]) )
    # DB.executeSql( "update \"TEST_MOBILE\" set \"MOBILE_NUM\" = CASE \"ID\" WHEN 1 THEN '13888888888' END where \"ID\" in (1)" )
    # DB.executeSql( "update TEST_MOBILE set MOBILE_NUM = '13888888888'")
    DB.close()
    return result

# NC财务脱敏
def other_mask_01(config):
    global dai_value
    DB = db.Db(config).strategy
    Masking = ms.Masking()

    count = DB.executeSql("select count(*) from gl_voucher")
    # count = 10000
    pageSize = 1000
    pageSum = int((count+pageSize-1)/pageSize)
    print("开始NC财务数据脱敏:共%s条待处理" % count)
    starttime = datetime.datetime.now()

    for page in range(pageSum):

        main_data = DB.executeSql("select  PK_VOUCHER,TOTALCREDIT,TOTALDEBIT from gl_voucher ORDER BY PK_VOUCHER DESC LIMIT %s,%s;" %(page*pageSize+1, pageSize))
        main_whenstr = ""
        main_instr = ""
        dai_whenstr = ""
        dai_instr = ""
        jie_whenstr = ""
        jie_instr = ""

        for i in main_data:
            # 生成主表随机金额
            new_value = Masking.getRandomNumber([10000,100000,4])
            new_value_F = new_value if i["TOTALCREDIT"] < 0 else -new_value
            new_value_F =round(new_value_F, 4)
            PK_VOUCHER = i["PK_VOUCHER"]

            # 主表更新语句条件
            main_whenstr += "WHEN '%s' THEN %s " % (PK_VOUCHER, new_value_F)
            main_instr += "'"+str(PK_VOUCHER)+"'" + ","



            # 根据主表查询子表贷方明细
            dai_data = DB.executeSql("select PK_DETAIL from gl_detail where pk_voucher='%s' and DIRECTION='C';" %(PK_VOUCHER))

            if len(dai_data) == 1:
                # 如果只有一条数据，主表金额等于贷方子表金额
                PK_DETAIL = dai_data[0]["PK_DETAIL"]
                dai_whenstr += "WHEN '%s' THEN %s " % (PK_DETAIL, new_value_F)
                dai_instr +=  "'"+str(PK_DETAIL)+"'" + ","
            elif len(dai_data) > 1:
                # 如果多条数据，主表金额拆分为多条子表金额
                sum = new_value
                for j in range(len(dai_data)):
                    if j == (len(dai_data)-1):
                        dai_value = sum
                    else:
                        dai_value = Masking.getRandomNumber([0,sum,4])
                        sum -= dai_value
                    PK_DETAIL = dai_data[j]["PK_DETAIL"]
                    dai_value_F = dai_value if new_value_F>0 else -dai_value
                    dai_value_F = round(dai_value_F, 4)
                    dai_whenstr += "WHEN '%s' THEN %s " % (PK_DETAIL,  dai_value_F)
                    dai_instr += "'"+str(PK_DETAIL)+"'" + ","



            # 根据主表查询子表借方明细
            jie_data = DB.executeSql("select PK_DETAIL from gl_detail where pk_voucher='%s' and DIRECTION='D';" %(PK_VOUCHER))

            if len(jie_data) == 1:
                # 如果只有一条数据，主表金额等于贷方子表金额
                PK_DETAIL = jie_data[0]["PK_DETAIL"]
                jie_whenstr += "WHEN '%s' THEN %s " % (PK_DETAIL, new_value_F)
                jie_instr += "'"+str(PK_DETAIL)+"'" + ","
            elif len(jie_data) > 1:
                # 如果多条数据，主表金额拆分为多条子表金额
                sum = new_value
                for k in range(len(jie_data)):
                    if k == (len(jie_data)-1):
                        jie_value = sum
                    else:
                        jie_value = Masking.getRandomNumber([0,sum,4])
                        sum -= jie_value
                    PK_DETAIL = jie_data[k]["PK_DETAIL"]
                    jie_value_F = jie_value if new_value_F>0 else -jie_value
                    jie_value_F = round(jie_value_F, 4)
                    jie_whenstr += "WHEN '%s' THEN %s " % (PK_DETAIL,  jie_value_F)
                    jie_instr += "'"+str(PK_DETAIL)+"'" + ","

            # for j in dai_data:



        # 更新主表
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
        "gl_voucher", "TOTALCREDIT", "PK_VOUCHER", main_whenstr, "PK_VOUCHER", main_instr[0:-1]))
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
            "gl_voucher", "TOTALDEBIT", "PK_VOUCHER", main_whenstr, "PK_VOUCHER", main_instr[0:-1]))

        # 更新贷方数据
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
            "gl_detail", "LOCALCREDITAMOUNT", "PK_DETAIL", dai_whenstr, "PK_DETAIL", dai_instr[0:-1]))
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
            "gl_detail", "CREDITAMOUNT", "PK_DETAIL", dai_whenstr, "PK_DETAIL", dai_instr[0:-1]))

        # 更新借方数据
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
            "gl_detail", "LOCALDEBITAMOUNT", "PK_DETAIL", jie_whenstr, "PK_DETAIL", jie_instr[0:-1]))
        DB.executeSql("update %s set %s = CASE %s %s END where %s in (%s)" % (
            "gl_detail", "DEBITAMOUNT", "PK_DETAIL", jie_whenstr, "PK_DETAIL", jie_instr[0:-1]))

        temptime = datetime.datetime.now()
        print("已处理%s条，待处理%s条，已用时%s秒！" %(pageSize*(page+1), count-pageSize*(page+1), (temptime-starttime).seconds))

        # print("主表SQL：update %s set %s = CASE %s %s END where %s in (%s)" % (
        # "gl_voucher", "TOTALCREDIT", "PK_VOUCHER", main_whenstr, "PK_VOUCHER", main_instr[0:-1]))
        # print("贷方SQL：update %s set %s = CASE %s %s END where %s in (%s)" % (
        #     "gl_detail", "LOCALCREDITAMOUNT", "PK_DETAIL", dai_whenstr, "PK_DETAIL", dai_instr[0:-1]))
        # print("借方SQL：update %s set %s = CASE %s %s END where %s in (%s)" % (
        #     "gl_detail", "LOCALDEBITAMOUNT", "PK_DETAIL", jie_whenstr, "PK_DETAIL", jie_instr[0:-1]))
    endtime = datetime.datetime.now()
    print("已脱敏完成！共用时%s秒！" % (endtime-starttime).seconds)
    DB.close()
    return 0