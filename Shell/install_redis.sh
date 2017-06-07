#!/usr/bin/env bash

#**********************************************
#File: install_redis.sh
#**********************************************
#Date: 2017-03-16
#**********************************************
#By : XUYONG
#**********************************************
#To : Auto install the redis
#**********************************************
#set -x
# ----- CONFIG -----
# redis下载地址
redis_link="http://download.redis.io/releases/"

# ---- FUNCTION ----
# 脚本使用帮助函数
function usage_help(){
echo -e """Usage:
\t${0/*\//} install\tInstall Redis
\t${0/*\//} config \tConfig Redis
\t\tconfig [install path] [port:6370] [number]
"""
}

# 获取redis版本帮助函数
function redis_version_help(){
    wget ${redis_link} -O /tmp/redis_tmp.txt >> /dev/null
    local version_list=$(cat /tmp/redis_tmp.txt |awk -F"href=\"" '{print $2}' | awk -F"\">" '{print $1}' | grep redis)
    for version in ${version_list[@]}:
    do
	echo -e "${version}"
    done
}


# 下载安装redis函数
function download_install(){
    local install_Dir=${1}
    local install_version=${2}
    # 下载tar包
    wget ${redis_link}redis-${install_version}.tar.gz -P ${install_Dir}
    # 解压缩
    tar -zxf ${install_Dir}/redis-${install_version}.tar.gz -C ${install_Dir} && mv  ${install_Dir}/redis-${install_version} ${install_Dir}/redis
    # 定义redis根目录 
    Dir=${install_Dir}/redis
    # 编译安装
    cd ${install_Dir}/redis && make && make install
	# 创建redis节点目录
	if [ ! -d ${install_Dir}/redis/cluster ];then
		mkdir  ${install_Dir}/redis/cluster
    fi
	# 设置环境变量
    sed -i '/\/data\/redis\/src/d' /etc/profile
    echo -e "PATH=\${PATH}:/data/redis/src/\t\t# redis  $(date)" >> /etc/profile && source /etc/profile
}

function config(){
	# 安装目录
	local install_Dir=${1:-"/data/redis"}
	# 启动端口基数
	local redis_port=${2:-"6379"}
	# 启动进程个数
	local redis_num=${3:-"1"}
	# bind IP
	IP=$(ip a | grep inet | grep -v 127.0.0.1 | awk '{print $2}')
	# conf main config
	if [ ! -f ${install_Dir}/cluster/comm_redis.conf ];then
		cat >> ${install_Dir}/cluster/comm_redis.conf <<EOF
daemonize yes
tcp-backlog 511
timeout 0
tcp-keepalive 0
loglevel notice
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-entries 512
list-max-ziplist-value 64
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes	
EOF
fi
for num in $(seq ${redis_num});do
	# 计算端口
	PORT=$[${redis_port}+${num}]
	mkdir ${install_Dir}/cluster/${PORT}
	if [ -f ${install_Dir}/cluster/${PORT}/redis.conf ];then
		mv ${install_Dir}/cluster/${PORT}/redis.conf ${install_Dir}/cluster/${PORT}/redis.conf.`date +%F`.bak
	fi
	cat >> ${install_Dir}/cluster/${PORT}/redis.conf <<EOF
include ${install_Dir}/cluster/comm_redis.conf
pidfile ${install_Dir}/cluster/${PORT}/redis_${PORT}.pid
port ${PORT}
bind ${IP/\/*/}
logfile ${install_Dir}/cluster/${PORT}/redis_${PORT}.log
dir ./
EOF
	# 启动服务
	${install_Dir}/src/redis-server ${install_Dir}/cluster/${PORT}/redis.conf
	echo "redis server cluster:${PORT} started"
	echo -e """INFO:
Main config :${install_Dir}/cluster/comm_redis.conf
pidfile     :${install_Dir}/cluster/${PORT}/redis_${PORT}.pid
Bind ip port:${IP/\/*/}:${PORT}
logfile     :${install_Dir}/cluster/${PORT}/redis_${PORT}.log
data_DIR    :${install_Dir}/cluster/${PORT}
"""
done
}

# ------ MAIN ------
case $1 in
	install)
		read -p "请输入安装目录[default:/data]:" install_Dir
		while [ -d ${install_Dir:-"/data"}/redis ]
		do
		    read -p "目录已存在，是否删除[y/n]:" check_1
		    if [ ${check_1}="y|Y|yes|Yes|YEs|YES|YeS" ];then
		        rm -rf ${install_Dir:-"/data"}/redis
		    else
		        read -p "请重新输入安装目录[default:/data]:" install_Dir
		    fi
		done
		
		
		read -p "请输入安装版本[default:3.0.6]" install_version
		read -p "请输入端口基数[default:6370]" redis_port
		read -p "请输入需要启动服务个数[default:1]" redis_number
		# 执行下载安装函数
		download_install ${install_Dir:-"/data"} ${install_version:-"3.0.6"}
		clear && echo -e \
		"""============================================
Redis_Version: ${install_version:-"3.0.6"}
Install_Dir: ${Dir}
============================================"""
		config ${install_Dir:-"/data/redis"} ${redis_port:="6370"} ${redis_number:-1}
		echo "============================================"
	;;
	config)
		# install_Dir
		install_Dir=${2}
		redis_port=${3}
		redis_number=${4}
		config ${install_Dir:-"/data/redis"} ${redis_port:-"6370"} ${redis_number:-"1"}
	;;

	*)
		usage_help
	;;
esac
