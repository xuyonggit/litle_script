# _*_ coding:utf-8 _*_
# 脚本：
# 以mongo中数据为标准更新mysql中对应的数据
# author：xuyong

import pymysql
import os
import pymongo



def conn():
    return pymysql.connect(
        host='',
        port=3306,
        user='',
        password='',
        database='',
        charset='utf8'
    )


def connmongo():
    return pymongo.MongoClient('mongohost', mongoport)


# 文件中读取id返回ID列表
def readfile():
    L1 = []
    with open('test.txt', 'r', encoding='UTF-8') as f:
        for i in f.readlines():
            D1 = {}
            lines = i.strip('\n')
            L1.append(lines.split()[1])
    return L1


# 根据ID列表获取mongo数据，返回字典格式
def getdatafrommongo(lists=[]):
    datalist = lists
    C = connmongo()
    db = C.person.person
    res_D = {}
    for queryid in datalist:
        res = db.find_one({"virtual": "0", "createUserId": int(queryid)}, {"portrait": 1})
        if res.get("portrait") != "" and res.get("portrait") != None:
            res_D[queryid] = res.get("portrait")
    return res_D


# 根据ID列表获取mysql数据，返回字典格式
def getdatafromysql(lists=[]):
    con = conn()
    cur = con.cursor()
    datalist = lists
    sql = "select pic_path from tb_user where id={};"
    res_D = {}
    for queryid in datalist:
        cur.execute(sql.format(queryid))
        for i in cur:
            if i[0] != "":
                res_D[queryid] = i[0]
    cur.close()
    con.close()
    return res_D


# 取两个字典中相同key不同value的数据，返回字典{key:d1-value}
def main(d1={}, d2={}):
    s = d1
    d = d2
    res_D = {}
    for queryid, querydata in s.items():
        if querydata != d[queryid]:
            res_D[queryid] = querydata
    return res_D


# 更新mysql数据库
def update(d1={}):
    con = conn()
    cur = con.cursor()
    sql = "update tb_user set pic_path='{}' where id={};"
    i = 0
    for userid,picpath in d1.items():
        cur.execute(sql.format(picpath, userid))
        print("update mysql >>> userid:{} - picpath: {}".format(userid, picpath))
        i += 1
        con.commit()
    print("update done, all update <{}>".format(i))


if __name__ == '__main__':
    L1 = readfile()
    readdata = readfile()
    mongodata = getdatafrommongo(lists=readdata)
    mysqldata = getdatafromysql(lists=readdata)
    update(main(mongodata, mysqldata))