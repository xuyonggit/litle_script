#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# **********************************************
# File: ipcount.py
# **********************************************
# Date: 2017-02-13
# **********************************************
# By :  XUYONG
# **********************************************
# To : 分类统计Jboss和Tomcat请求日志中的IP，输出到excel表格
# Usage: python ipcount.py  日志路径  生成的xls文件
# **********************************************
# -- import & config --
import xlwt
import re
import os, sys
# =========== CONFIG ================
# log DIR
log_dir = sys.argv[1]
excel_name = sys.argv[2]
# ============= END ==================
# function
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()      #初始化样式
    font = xlwt.Font()      # 为样式创建字体
    font.name = name
    font.bold = bold        # 加粗
    font.color_index = 4
    font.height = height
    style.font = font
    return style
# 创建Excel
xls_file = xlwt.Workbook()
table = xls_file.add_sheet(u'请求IP统计')
title = [u'日期', u'请求IP', u'请求次数']
# 写入标题
for i in range(3):
    table.write(0, i, title[i])

FILES = os.listdir(log_dir)
FILES.sort()
# 定义Excel行
hang = 1
for FILE in FILES:
    DATE = re.sub('-', '', FILE.split('.')[1])
    table.write(hang, 0, DATE)
    FILEPATH = log_dir + '/' + FILE
    with open(FILEPATH) as f:
       DATE = {}
       for r in f.readlines():
           IPS = re.findall('(.*?) -.*?', r)[0]
           if IPS not in DATE.keys():
               DATE[IPS] = 1
           else:
               DATE[IPS] = DATE[IPS] + 1
    for ip in DATE.keys():
        table.write(hang, 1, ip)
        table.write(hang, 2, DATE[ip])
        hang = hang + 1
xls_file.save(excel_name)