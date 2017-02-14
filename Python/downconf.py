#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# 注意：python2.X
# **********************************************
# File: downconf.py
# **********************************************
# Date: 2017-02-13
# **********************************************
# By :  XUYONG
# **********************************************
# To : Download config files
# **********************************************
# -- import & config --
import os, sys
import smtplib
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import mimetypes
import email.MIMEImage
jboss_config_dic = {'config.properties':'/standalone', 'standalone.xml':'/standalone/configuration', 'flights.properties':'/standalone'}
tomcat_config_dic = []

# -- function --
def download(host, name, path):
    os.system('scp operator@%s:%s /data/workon/data/download/' % (host, path))
    return '/data/workon/data/download/' + name
# -- END --


# -- main --
# 定义信息字典
dic = {}
# 获取IP地址
ipaddr = raw_input('请输入主机地址：')
while not ipaddr:
    ipaddr = raw_input('请输入正确的主机地址：')
dic['ip'] = ipaddr
# 获取服务类型
servertype = raw_input('请选择服务类型：\n1）Jboss\n2）Tomecat\n请输入序号选择：')
while not servertype:
    servertype = raw_input('请输入正确的序号选择：')
# 获取服务序号或标识
servernum = raw_input('请输入服务对应的序号或标识：')
while not servernum:
    servernum = raw_input('请输入服务对应的序号或标识：')
dic['num'] = servernum
# 获取配置文件名
num = 1
if servertype == '1':
    for i in jboss_config_dic.keys():
        print(str(num) + ')' + i)
        num += 1
    configfilename = raw_input('请选择需要下载的配置文件[请选择序号]：')
    dic['server'] = 'jboss'
    dic['config'] = jboss_config_dic.keys()[int(configfilename) - 1]
    server = dic['server'] + dic['num']
    filepath = '/data/opt/' + dic['server'] + dic['num'] + jboss_config_dic[dic['config']] + '/' + dic['config']
elif servertype == '2':
    for i in tomcat_config_dic.keys():
        print(str(num) + ')' + i)
        num += 1
    configfilename = raw_input('请选择需要下载的配置文件[请选择序号]：')
    dic['server'] = 'tomcat'
    dic['config'] = tomcat_config_dic.keys()[int(configfilename) - 1]
    server = dic['server'] + dic['num']
    filepath = '/data/opt/' + dic['server'] + dic['num'] + tomcat_config_dic[dic['config']] + '/' + dic['config']
else:
    print('Error')
# 获取收件人地址
mailTO = raw_input('请输入附件接受人地址[";"隔开]：')
while not mailTO:
    mailTO = raw_input('请输入附件接受人地址[";"隔开]：')
dic['mailto'] = mailTO

os.system('clear')
print('***********************************************')
print('\033[4;31m录入信息:\033[0m')
print('***********************************************')
print('\033[3;34m主 机 : \033[0m' + dic['ip'] + '\n\033[3;34m服 务 : \033[0m' + server + '\n\033[3;34m路 径 : \033[0m' + filepath + '\n\033[3;34m接收人: \033[0m' + dic['mailto'])
print('***********************************************')
sure_status = raw_input('请确定以上内容，如正确请输入【y】继续，输入其他则退出：')
if sure_status != 'y':
    os.system('exit')
else:
    content = download(dic['ip'], dic['config'], filepath)
    From = 'xuyong@shijie99.com'
    To = dic['mailto']
    file_name = content

    server = smtplib.SMTP('smtp.qiye.163.com')
    server.login('xuyong@shijie99.com', 'Aichang021')

    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = email.MIMEText.MIMEText('附上所需配置文件', _charset='utf-8')
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    ctype,encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_msg = email.MIMEImage.MIMEImage(open(file_name, 'rb').read(), subtype)

    # 设置附件头
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition','attachment', filename = basename)
    main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = From
    main_msg['To'] = dic['mailto']
    main_msg['Subject'] = "配置文件"
    main_msg['Date'] = email.Utils.formatdate()

    # 得到格式化后的完整文本
    fulltext = main_msg.as_string()

    try:
        server.sendmail(From, To, fulltext)
    finally:
        server.quit()