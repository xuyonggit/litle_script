#!/usr/bin/python3
# -*-coding: utf-8-*-
# 发送微信消息脚本

# IMPORT =========================================
import requests
import json
import os, sys
import logging

# CONFIG =========================================
# 定义log目录与级别
logging.basicConfig(filename = '/data/zabbix/logs/send_weixin.log', level = logging.INFO)
# 定义认证corpid
corp = {
'corpid': '', 
'corpsecret': ''
}
# FUNCTION =======================================
def get_token():
	url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid='+corp['corpid']+'&corpsecret='+corp['corpsecret']
	req = requests.get(url)
	data = json.loads(req.text)
	return data['access_token']

def send_msg(CONTENT):
	url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
	values = """{
		"toparty": "2",
		"msgtype": "text",
		"agentid": 1,
		"text":{
			"content": "%s",
		},"safe": "0"
	}""" % str(CONTENT)
	logging.info("MESSAGE:"+values)
	req = requests.post(url, data=values)
	logging.info(req.text)

if __name__ == "__main__":
	EVENT_ID = sys.argv[2]
	logging.info("EVENT_ID:"+EVENT_ID)
	CONTENT = sys.argv[3]
	send_msg(CONTENT)
