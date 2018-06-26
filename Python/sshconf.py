# -*- coding:utf-8 -*-
# desc: 展示~/.ssh/config文件中服务器信息，并从redis获取对应外网地址以及主机名
# redis : alias - "{'hostname': '', 'address': ''}"
# auther: xuyong
import os, sys
import re
import redis
from prettytable import PrettyTable

def help():
    print('Usage:\n\t%s --list  \033[33mshow config info\033[0m' % sys.argv[0])


def con():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    return redis.Redis(connection_pool=pool)


def list():
    homepath = os.environ['HOME']
    dic = {}
    with open('{}/.ssh/config'.format(homepath), 'r') as f:
        for i in f.readlines():
            if "Host " in i:
                name = re.findall('Host (.*)', i)[0]
                dic[name] = {}
                dic[name].setdefault('Hostname', '\033[31mNone\033[0m')
                dic[name].setdefault('Inip', '\033[31mNone\033[0m')
                dic[name].setdefault('address', '\033[31mNone\033[0m')
                dic[name].setdefault('User',  'root')
                dic[name].setdefault('Port',  22)
                dic[name].setdefault('IdentityFile',  '~/.ssh/id_rsa')
                dic[name].setdefault('IdentitiesOnly',  'yes')
                Con = con()
                redis_data_info = Con.get(name)
                if redis_data_info:
                    s = eval(redis_data_info)
                    dic[name]['Hostname'] = s.get('hostname', '\033[31mNone\033[0m')
                    dic[name]['address'] = s.get('address', '\033[31mNone\033[0m')
            elif "Hostname " in i:
                dic[name]['Inip'] = re.findall('Hostname (.*)', i)[0]
            elif "Port " in i:
                dic[name]['Port'] = re.findall('Port (.*)', i)[0]
            elif "User " in i:
                dic[name]['User'] = re.findall('User (.*)', i)[0]
            elif "IdentityFile " in i:
                dic[name]['IdentityFile'] = re.findall('IdentityFile (.*)', i)[0]
            elif "IdentitiesOnly " in i:
                dic[name]['IdentitiesOnly'] = re.findall('IdentitiesOnly (.*)', i)[0]
#   print("======================================================================")
#   print("Alias\tHostname\tUser\tPort\tIdentityFile\tIdentitiesOnly")
#   print("======================================================================")
    x = PrettyTable(['别名', '主机名', '内网IP', '外网IP', '用户', '端口', 'IdentityFile', 'IdentitiesOnly'])
    for keys in dic.keys():
        List1 = []
        List1.append(keys)
        List1.append(dic[keys]['Hostname'])
        List1.append(dic[keys]['Inip'])
        List1.append(dic[keys]['address'])
        List1.append(dic[keys]['User'])
        List1.append(dic[keys]['Port'])
        List1.append(dic[keys]['IdentityFile'])
        List1.append(dic[keys]['IdentitiesOnly'])
        x.add_row([List1[0], List1[1], List1[2], List1[3], List1[4], List1[5], List1[6], List1[7]])
    x.align['主机名'] = 'l'
    # 打印表格并排序第一列
    print(x.get_string(sortby='别名'))
# main
try:
    if sys.argv[1] == '--list':
        list()
    else:
        help()
except IndexError as e:
    help()
