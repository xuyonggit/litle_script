#!/usr/bin/env bash
# **********************************************
# File: ggjboss.sh
# **********************************************
# Date: 2017-02-08
# **********************************************
# By : XUYONG
# **********************************************
# To : 启动，停止，重启jboss
# **********************************************
set -x
#============================== config =================================
# 获取当前时间
LOGTIME=`date -d "0 days ago" +"%Y%m%d%H%M%S"`
# 服务安装目录
SERVERDIR="/data/opt"


#============================== function =================================
# 帮助函数：
function help(){
echo -e """
Usages:
            ${0} start 服务序号（不限个数）    启动一个或多个服务
            ${0} stop  服务序号（不限个数）    停止一个或多个服务
            ${0} restart 服务序号（不限个数）  重启一个或多个服务
"""
}

# 启动函数
function start(){
# 参数为空时：
if [[ "$1" = "" ]];then
# 获取PID
    PID=`ps -ef | grep -v grep | grep "/jboss1/"|sed -n  '1P' | awk '{print $2}'`
    export JBOSS_HOME=${SERVERDIR}/jboss1
# 参数不为空时：
else
    PID=`ps -ef | grep -v grep | grep "/jboss"$1"/"|sed -n  '1P' | awk '{print $2}'`
    export JBOSS_HOME=${SERVERDIR}/jboss"$1"
fi
if [ -z ${PID} ];then
    cd ${JBOSS_HOME}/standalone
    ${JBOSS_HOME}/bin/standalone.sh > /dev/null &
    rm -f /logs/jboss1.log
    ln -s ${JBOSS_HOME}/standalone/log/server.log /logs/jboss1.log
    echo "启动${JBOSS_HOME##*/}......"
else
    echo "{JBOSS_HOME##*/}已启动，PID：${PID}"
fi

}

# 停止函数
function stop(){
if [[ "$1" = "" ]]; then
    export JBOSS_HOME="/data/opt/jboss1"
else
    export JBOSS_HOME="/data/opt/jboss"$1""
fi
ps aux | grep -v grep | grep "${JBOSS_HOME}""/" | awk '{print $2}' | xargs kill -9
cd ${JBOSS_HOME}/standalone/tmp
rm -rf vfs/*
ps aux | grep "${JBOSS_HOME}""/"

}






#============================== main =================================
case $1 in
    start)  # 启动
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            start ${i}
            sleep 2
        fi
    done
    ;;
    stop)   # 停止
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            stop ${i}
            sleep 2
        fi
    done
    ;;
    restart)    # 重启
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            stop ${i}
            sleep 3
            start ${i}
        fi
    done
    ;;
    *)help
    ;;
esac