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

#============================== config =================================
# 获取当前时间
LOGTIME=`date -d "0 days ago" +"%Y%m%d%H%M%S"`
# 服务安装目录
SERVERDIR="/data/opt"


#============================== function =================================
# 帮助函数：
function help(){
echo -e """Hello,大家好，我叫小智。
\033[33m小智提醒：\033[0mUsages:
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
    rm -f /logs/"${JBOSS_HOME##*/}".log
    ln -s ${JBOSS_HOME}/standalone/log/server.log /logs/"${JBOSS_HOME##*/}".log
    echo -e "\033[33m小智提醒： \033[0m正在启动"${JBOSS_HOME##*/}"中......"
    sleep 2
    # 判断服务状态
    ps aux | grep "${JBOSS_HOME}""/" | grep -v grep > /dev/null && echo -e "\033[33m小智提醒： \033[0m"${JBOSS_HOME##*/}"服务已成功启动。。。" || echo -e "\033[33m小智提醒： \033[0m"${JBOSS_HOME##*/}"服务启动失败，请尝试手动启动。。。"
else
    echo -e "\033[33m小智提醒： \033[0m"${JBOSS_HOME##*/}"已启动，PID：${PID}"
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
echo -e "\033[33m小智提醒： \033[0m正在停止"${JBOSS_HOME##*/}"......"
sleep 2
# 删除缓存
cd ${JBOSS_HOME}/standalone/tmp
rm -rf vfs/*
# 删除日志链接文件
rm -f /logs/"${JBOSS_HOME##*/}".log
# 判断服务状态
ps aux | grep "${JBOSS_HOME}""/" | grep -v grep > /dev/null && echo -e "\033[33m小智提醒： \033[0m"${JBOSS_HOME##*/}"服务停止失败，请尝试手动kill。。。" || echo -e "\033[33m小智提醒： \033[0m"${JBOSS_HOME##*/}"服务已成功停止。。。"

}


#============================== main =================================
case $1 in
    start)  # 启动
    echo "============================================================"
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            start ${i}
        fi
        echo
    done
    echo "============================================================"
    ;;
    stop)   # 停止
    echo "============================================================"
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            stop ${i}
            sleep 2
        fi
        echo
    done
    echo "============================================================"
    ;;
    restart)    # 重启
    echo "============================================================"
    for i in $*
    do
        if [[ ${i} != $1 ]];then
            stop ${i}
            sleep 3
            start ${i}
        fi
        echo
    done
    echo "============================================================"
    ;;
    *)help
    ;;
esac