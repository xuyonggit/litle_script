#!/bin/bash
# Author : Xu Yong
# Desc : 自动监控tomcat进程并异常重启脚本
# Date : 2017-07-24

# 监控服务列表
TOMCAT_LIST=(tomcat1 tomcat2 tomcat3)
# 扫描间隔时间(s)
TIME_STOP='10'
# tomcat启动脚本(绝对路径)
SCRIPT_PATH="/opt/monitor/sbin/ggtomcat.sh"



# ===============================================================
# =================    下列勿动   后果自负  =====================
# ===============================================================
# main
while [ 1 ];do
	for SERVICE in ${TOMCAT_LIST[@]};do
		N=$(ps -ef | grep "/${SERVICE}/" | grep -v grep | wc -l)
		if [ ${N} -eq 0 ];then
			echo "[ $(date +"%F %T") ] service ${SERVICE} done"
			sh ${SCRIPT_PATH} start ${SERVICE/tomcat/} 2>&1 >/dev/null
		else
			echo "[ $(date +"%F %T") ] service ${SERVICE} active"
		fi
	done
	sleep ${TIME_STOP}
done
