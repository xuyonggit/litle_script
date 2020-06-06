# -*- coding: utf-8 -*-
#   Copyright (C) 2020 All rights reserved.
#
#  FileName      ：upload.py
#  Author        ：xuyong1
#  Email         ：xuyong1@kingsoft.com
#  Date          ：2020年06月05日
#  Description   ：
#

import datetime
import poplib
import email
from email.parser import Parser
from email.header import decode_header
import configparser
import os
import sys
import telnetlib
import time
import paramiko
from scp import SCPClient
from opstools2.wechat.wechat_api import WechatApi


class get_email(object):
    def __init__(self):
        self.config = configparser.RawConfigParser()
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.conf')
        if not os.path.isfile(path):
            print("未找到配置文件: {}".format(path))
            sys.exit()
        self.config.read(path)

        self.user = self.config.get('download', 'user')
        self.pwd = self.config.get('download', 'password')
        self.server = self.config.get('download', 'server')
        self.sender = self.config.get('download', 'sender')
        self.filepath = self.config.get('download', 'filepath')
        self.remote_host = self.config.get('download', 'remote_host')
        self.remote_port = int(self.config.get('download', 'remote_port'))
        self.remote_user = self.config.get('download', 'remote_user')
        self.remote_key = self.config.get('download', 'remote_key')
        self.notify_name = self.config.get('download', 'notify_name')
        self.CORP_ID = self.config.get('download', 'CORP_ID')
        self.APP_ID = self.config.get('download', 'APP_ID')
        self.APP_SECRET = self.config.get('download', 'APP_SECRET')
        self.attachment_files = []
        self.wechatconf = {
                'NAME': '金山小额',
                'CORP_ID': self.CORP_ID,
                'APP_LIST': {
                    'upload_robot': {
                        'APP_ID': self.APP_ID,
                        'APP_SECRET': self.APP_SECRET,
                        'switch': 'on'
                        }
                    }
                }

    @staticmethod
    def decode_str(str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

    def get_att(self, msg_in, stime):
        for part in msg_in.walk():
            file_name = part.get_filename()
            if file_name:
                h = email.header.Header(file_name)
                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    filename = self.decode_str(str(filename, dh[0][1]))

                # 下载附件
                data = part.get_payload(decode=True)
                with open('{}{}_{}'.format(self.filepath, stime, filename), 'wb') as w:
                    self.attachment_files.append('{}{}_{}'.format(self.filepath, stime, filename))
                    print('downloading file {}'.format(filename))
                    w.write(data)

    def upload_file(self):
        private_key = paramiko.RSAKey.from_private_key_file(self.remote_key)
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.remote_host, port=self.remote_port, username=self.remote_user, pkey=private_key)
            with SCPClient(ssh.get_transport(), socket_timeout=15.0) as scp:
                try:
                    for f in self.attachment_files:
                        scp.put(str(f), '/home/shenyingdong_jump_linux/' + f.split(os.sep)[-1])
                        os.remove(str(f))
                except Exception as e:
                    print(e)
        self.send_notify()

    def send_notify(self):
        we = WechatApi(self.wechatconf)
        status, res = we.apps['upload_robot'].send(
                msg_type='text',
                to_users_list=self.notify_name.split(','),
                msg_string='''您提交的文件：{} 已完成上传
请登录服务器在家目录(cd ~/)查看
'''.format(','.join(x.split(os.sep)[-1] for x in self.attachment_files))
                )

    def run_ing(self):
        _day = (datetime.datetime.now() - datetime.timedelta(minutes=11)).strftime('%Y%m%d%H%M')
        try:
            telnetlib.Telnet(self.server, 995)
            server = poplib.POP3_SSL(self.server, 995, timeout=10)
        except Exception:
            time.sleep(5)
            server = poplib.POP3(self.server, 110, timeout=10)

        server.user(self.user)
        server.pass_(self.pwd)
        resp, mails, octets = server.list()
        _index = len(mails)

        for i in range(_index, 0, -1):
            resp, lines, octets = server.retr(i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            _date = time.strftime("%Y%m%d%H%M", time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S'))
            if _date < _day:
                break
            else:
                if msg.get('From').split('@')[0] in self.sender.split(',') and msg.get('Cc').split()[0] in ['xuyong1@kingsoft.com', 'xuyong1@wps.cn']:
                    self.get_att(msg, _date)
        server.quit()
        print("file list : {}".format(self.attachment_files))
        if self.attachment_files:
            self.upload_file()


if __name__ == '__main__':
    C = get_email()
    C.run_ing()