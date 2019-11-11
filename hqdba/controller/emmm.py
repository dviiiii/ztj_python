import json
from django.http import JsonResponse
import hqdba.db.Db as db
import hqdba.config.mysql_config as config

# 新增任务
def get_emmm_list(request):
    params = json.loads(request.body)
    pagesize = params['pagesize']
    pagenum = (params['pagenum']-1)*pagesize + 1
    target = params['target']
    name = params['name']
    ismsk = params['ismsk']
    if ismsk == 'all':
        ismsk = '0 or fh_ismsk = 1)'
    else:
        ismsk += ')'

    target_sql = '''select fh_name, c.fh_code, fh_date, fh_ismsk, target_name from (select fh_name, a.fh_code, fh_date,fh_ismsk 
            from fh_fact a join target_dim b 
            on a.fh_code = b.fh_code 
            where target_name like "%{}%"
            and fh_name like "%{}%"
            and (fh_ismsk = {} group by fh_name, a.fh_code, fh_date,fh_ismsk limit {},{}) c
            join target_dim d on c.fh_code = d.fh_code'''.format(target, name, ismsk, pagenum, pagesize)

    magnet_sql = '''select fh_name, c.fh_code, fh_date, fh_ismsk, 
            magnet_url, magnet_name, magnet_size, magnet_date
            from (select fh_name, a.fh_code, fh_date,fh_ismsk 
            from fh_fact a join target_dim b 
            on a.fh_code = b.fh_code 
            where target_name like "%{}%"
            and fh_name like "%{}%"
            and (fh_ismsk = {} group by fh_name, a.fh_code, fh_date,fh_ismsk limit {},{}) c
            join url_dim e on c.fh_code = e.fh_code'''.format(target, name, ismsk, pagenum, pagesize)

    count_sql = '''select count(*) as total from (select fh_name, a.fh_code, fh_date,fh_ismsk
            from fh_fact a join target_dim b 
            on a.fh_code = b.fh_code 
            where target_name like "%{}%"
            and fh_name like "%{}%"
            and (fh_ismsk = {} group by fh_name, a.fh_code, fh_date,fh_ismsk) tb'''.format(target, name, ismsk, pagenum, pagesize)

    targetdata = get2db(target_sql)
    magnetdata = get2db(magnet_sql)
    total = get2db(count_sql)
    print(target_sql)

    data = []
    obj = {}
    for i in targetdata:
        fh_code = i['fh_code'].replace('-', '_')
        if not fh_code in obj.keys():
            obj[fh_code] = {}
            obj[fh_code]['fh_name'] = i['fh_name']
            obj[fh_code]['fh_code'] = i['fh_code']
            obj[fh_code]['fh_date'] = i['fh_date']
            obj[fh_code]['fh_ismsk'] = i['fh_ismsk']
            obj[fh_code]['fh_target'] = []
            obj[fh_code]['fh_target'].append(i['target_name'])
        else:
            obj[fh_code]['fh_target'].append(i['target_name'])

    for i in magnetdata:
        fh_code = i['fh_code'].replace('-', '_')
        if not 'fh_magent' in obj[fh_code].keys():
            obj[fh_code]['fh_magent'] = []
            obj[fh_code]['fh_magent'].append({
                'magnet_url': i['magnet_url'],
                'magnet_name': i['magnet_name'],
                'magnet_size': i['magnet_size'],
                'magnet_date': i['magnet_date']
            })
        else:
            obj[fh_code]['fh_magent'].append({
                'magnet_url': i['magnet_url'],
                'magnet_name': i['magnet_name'],
                'magnet_size': i['magnet_size'],
                'magnet_date': i['magnet_date']
            })

    for i in obj.keys():
        data.append(obj[i])

    return JsonResponse({'list': data, 'total': total[0]['total']})


def get_emmm_target(request):
    sql = 'select target_name,count(*) as num from target_dim group by target_name order by count(*) desc'
    data = get2db(sql)
    return JsonResponse({'list': data})


def get2db(sql):
    dbconfig = config.default_config2()
    DB = db.Db(dbconfig).strategy
    data = DB.executeSql(sql)
    DB.close()
    return data
