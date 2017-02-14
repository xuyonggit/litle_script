#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# 注意：python2.X
# **********************************************
# File: search.py
# **********************************************
# Date: 2017-02-13
# **********************************************
# By :  XUYONG
# **********************************************
# To : 搜索查询脚本
# Usage: 需与serverfile.sh关联
# **********************************************
import os, sys
import re
# 获取数据文件列表
filelist = os.listdir('/data/workon/data/serverfiledate')

# 帮助函数
def help():
    print "Usage:"
    print "\t# search [搜索的内容]"
    print "\t# -help  Get help"

if len(sys.argv) != 2 or sys.argv[1] == '-help':
    help()
    sys.exit()
else:
    var = sys.argv[1]
# 定义数据字典
searchdatalist = {}

for i in filelist:
    out = os.popen('cat /data/workon/data/serverfiledate/%s | grep -i %s' % (i,var))
    searchdatalist[i] = re.sub(var, '\033[1;31m%s\033[0m\033[33m' % var, out.read())

for i in searchdatalist.keys():
    if searchdatalist[i] == '':
        del searchdatalist[i]
os.system('clear')

# 搜索结果为空显示：
if len(searchdatalist) == 0:
    print "\033[1;34m主机:\033[0m NULL:\t" + "\033[1;34m目录:\033[0m NULL:"
    print "*************************************************************************"
    print "\033[5;31m没有符合要求的数据!\033[0m"

# 搜索结果不为空显示：
for i in sorted(searchdatalist.keys()):
    dir1 = i.split("_")[0]
    IP = i.split("_")[1]
    print "\033[1;34m主机:\033[0m %s:\t" % IP + "\033[1;34m目录:\033[0m %s:" % dir1
    print "*************************************************************************"
    print '\033[33m' + searchdatalist[i] + '\033[0m'