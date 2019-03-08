#!/usr/bin/env python
# desc：远程执行shell命令，附件发送邮件，抄送
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os, sys

import paramiko
from jinja2 import Environment, FileSystemLoader


class Smail():
    def __init__(self, filepath, toaddres, vpnusername, vpnpassword):
        self.smtpserver = 'smtp.exmail.qq.com'
        self.user = 'system@gintong.com'
        self.password = 'gt123UPUP'
        self.From = 'system@gintong.com'
        self.To = toaddres
        self.Filepath = filepath

        # title
        self.subject = 'system send'

        # datas
        self.data = {'username': vpnusername, 'password': vpnpassword, 'psk': 'gintong'}

        # jinja2 env
        self.env = Environment(loader=FileSystemLoader(os.path.join('other', 'vpn-usermanager'), encoding='utf-8'))

        # body
        self.template = self.env.get_template('main.html')
        self.bodys = self.template.render(data=self.data)

    def openFile(self, filepath):
        with open(filepath, 'rb') as f:
            mail_body = f.read()
            msg = MIMEApplication(mail_body)
            # 指定当前文件格式类型
            msg.add_header('Content-type', 'application/msword')
            msg.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', filepath.split(os.path.sep)[-1]))
            return msg

    def sendMail(self):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.From
        msgRoot['To'] = self.To
        msgRoot['cc'] = 'lixuguang@gintong.com'
        msgRoot.attach(MIMEText(self.bodys, 'html', 'utf-8'))
        for filepath in self.Filepath:
            msgRoot.attach(self.openFile(filepath))

        smtp_server = smtplib.SMTP()
        #smtp_server.set_debuglevel(1)
        smtp_server.connect(self.smtpserver, '25')
        smtp_server.login(self.user, self.password)
        smtp_server.sendmail(self.From, self.To, msgRoot.as_string())
        smtp_server.quit()
        print("send email successful")

    def ssh_connect(self, _host='192.168.101.89', _username='root', password='Gintong.com'):
        adduser = self.data['username']
        addpass = self.data['password']
        try:
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(_host, 22, _username, password)
        except Exception as e:
            print('errrrrrrrrrrrrrr')
            print('ssh {}@{}: {}'.format(_username, _host, e))
            exit()
        else:
            _in0, _out0, _err0 = _ssh_fd.exec_command("cat /etc/ppp/chap-secrets| grep -v ^# | awk '{print $1}'")
            out0 = [x.strip() for x in _out0.readlines()]
            if adduser in out0:
                print("errrrrrrrrrrr: 用户：{} 已存在，创建失败".format(adduser))
                sys.exit(1)
            _in, _out, _err = _ssh_fd.exec_command(
                "sed -i '$a{} * \"{}\" *' /etc/ppp/chap-secrets".format(adduser, addpass))
            if len(_err.readlines()) > 0:
                print("errrrrrrrrrrrr: ", _err)
            # reload service
            _in1, _out1, _err1 = _ssh_fd.exec_command("service xl2tpd restart")
            if len(_err.readlines()) > 0:
                print("errrrrrrrrrrrr: ", _err1)


# 检查收件人邮箱
def checkEmail(toaddres):
    return toaddres


if __name__ == '__main__':

    mail_to = checkEmail(sys.argv[1])
    vpn_username = sys.argv[2]
    vpn_password = sys.argv[3]

    Filepath = [os.path.join('other', 'vpn-usermanager', '金桐vpn安装手册for_mac.doc'),
                os.path.join('other', 'vpn-usermanager', '金桐vpn安装手册for_windows.doc')
                ]

    #Filepath = ['金桐vpn安装手册for_mac.doc', '金桐vpn安装手册for_windows.doc']
    smail = Smail(Filepath, mail_to, vpn_username, vpn_password)
    # 增加用户操作
    smail.ssh_connect()
    smail.sendMail()
