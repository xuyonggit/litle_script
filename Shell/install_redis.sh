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
	mkdir  ${install_Dir}/redis/cluster
    # 设置环境变量
    sed -i '/\/data\/redis\/src/d' /etc/profile
    echo -e "PATH=\${PATH}:/data/redis/src/\t\t# redis  $(date)" >> /etc/profile && source /etc/profile
}

function config(){
	pass
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
		# 执行下载安装函数
		download_install ${install_Dir:-"/data"} ${install_version:-"3.0.6"}
		clear && echo -e \
		"""============================================
Redis_Version: ${install_version:-"3.0.6"}
Install_Dir: ${Dir}
============================================
是否进行redis配置[y/n]: """
		read check_2
		if [ ${check_2}="y|Y|yes|Yes|YEs|YES|YeS" ];then
		    continue
		else
		    exit
		fi
		echo "continue"
	;;


	*)
		usage_help
	;;
esac
