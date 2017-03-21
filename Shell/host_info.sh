#!/usr/bin/env bash
# **********************************************
# File: host_info.sh
# **********************************************
# Date: 2017-03-21
# **********************************************
# By : XUYONG
# **********************************************
# To : 获取主机基本信息
# **********************************************
# config
info_null="\033[31;5m未知\033[0m"
# get hostname 
info_hostname=${HOSTNAME}

# get user info
info_username=$(whoami)

# get IP
info_ip=$(/sbin/ip a | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}')

# get kernel name
info_kernel_name=$(uname)

# get now time
info_nowtime=$(date +%F" "%X)

# get kernel version
info_kernel_version=$(uname -r)

# ******** CPU INFO
# get cpu processor
info_cpu_processor=$(grep "processor" /proc/cpuinfo | wc -l)

# get cpu cores
info_cpu_cores=$(grep "cpu cores" /proc/cpuinfo | uniq |awk -F":" '{print $2}'|sed -e 's/^ //')

# get cpu core(MAX)
info_cpu_cores_max=$(grep "siblings" /proc/cpuinfo |uniq | awk -F":" '{print $2}'|sed -e 's/^ //')

# 判断是否启用超线程
if [ ${info_cpu_cores_max:-0} = 0 -o ${info_cpu_cores:-0} = 0 ];then
    pass
elif [ ${info_cpu_cores_max:-0} = ${info_cpu_cores:-0} ];then
    info_cpu_ltcores="是"
else
    info_cpu_ltcores="否"
fi

# ******** MEM INFO
# get MemTotal
info_mem_Total=$(grep "MemTotal" /proc/meminfo | awk '{printf("%.2f\n",$2/1024/1024)}')

# get swapTotal
info_mem_swapTotal=$(grep "SwapTotal" /proc/meminfo | awk '{printf("%.2f\n",$2/1024/1024)}')

# ******** Other INFO
info_selinux=$(getenforce)
# print info
clear && echo -e """*************** INFO ***************
\033[33m当前用户: \033[0m${info_username:-"${info_null}"}
\033[33m主机名  : \033[0m${info_hostname:-"${info_null}"}
\033[33m当前时间: \033[0m${info_nowtime:-"${info_null}"}
\033[33mIP地址  : \033[0m${info_ip:-"${info_null}"}
\033[33m内核类型: \033[0m${info_kernel_name:-"${info_null}"}
\033[33m内核版本: \033[0m${info_kernel_version:-"${info_null}"}
----- CPU INFO -----
\033[33mCPU逻辑核: \033[0m${info_cpu_processor:-"${info_null}"}
\033[33mCPU物理核: \033[0m${info_cpu_cores:-"${info_null}"}
\033[33m支持超线程: \033[0m${info_cpu_ltcores:-"${info_null}"}
----- MEM INFO -----
\033[33m最大内存: \033[0m${info_mem_Total:-"${info_null}"} "G"
\033[33mSwap大小: \033[0m${info_mem_swapTotal:-"${info_null}"} "G"
----- Other INFO -----
\033[33mSelinux: \033[0m${info_selinux:-"${info_null}"} 

*************** END ***************"""

