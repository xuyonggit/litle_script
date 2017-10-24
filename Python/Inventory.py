# _*_ coding:utf-8 _*_
# 脚本参数自定义方法

import argparse
import sys
import json


def hosts():
    r = {}
    h = ['192.168.1.10' + str(i) for i in range(1, 4)]
    hosts = {'hosts': h}
    r['docker'] = hosts
    return json.dumps(r, indent=4)


def lists(name):
    r = {'ansible_ssh_pass': '123456'}
    cis = dict(r.items())
    return json.dumps(cis)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='hosts list', action='store_true')
    parser.add_argument('-h', '--help', help='hosts vars')
    args = vars(parser.parse_args())

    if args['list']:
        print(lists())
    elif args['host']:
        print(hosts())
    else:
        parser.print_help()