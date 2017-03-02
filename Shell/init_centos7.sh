#!/usr/bin/env bash
# **********************************************
# File: init_centos7.sh
# **********************************************
# Date: 2017-02-08
# **********************************************
# By : XUYONG
# **********************************************
# To : 初始化centos7系统
# **********************************************
#conf
#读入ip
read -p "输入本机的ip: " ip_addr
read -p "输入本机的网关: " gateway
#取网卡设备号
eth_name=ifcfg-$(ip a s|grep "BROADCAST"|awk -F": " '{print $2}')
#取uuid
uuid_name=$(nmcli con | awk '$1 == "eno16777984" {print $2}')

###########################################################################
#关闭selinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g'  /etc/selinux/config

#关闭防火墙
systemctl disable iptables
systemctl disable firewall

#配置网卡
cat > /etc/sysconfig/network-scripts/$eth_name <<EOF
NAME="$eth_name"
TYPE="Ethernet"
BOOTPROTO="static"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
UUID="$uuid_name"
DEVICE="$eth_name"
ONBOOT="yes"
IPADDR="$ip_addr"
NETMASK=255.255.255.0
GATEWAY="$gateway"
EOF

echo 'nameserver 8.8.8.8' >> /etc/resolv.conf

#重启网卡
systemctl restart network

#安装必要软件
yum install -y  rsync net-tools openssh-clients vim

#rync同步工具
/usr/bin/rsync -avz --delete --port=2873 monitor@192.168.8.2::monitor /opt/monitor
/usr/bin/rsync -avz --delete --port=2873 cacti@192.168.5.123::cacti /opt/kingsoft


#创建operator家目录
mkdir -p /home/operator/.ssh
/usr/bin/cp -r /etc/skel/.bash* /home/operator/
chown -R operator:wheel /home/operator
usermod -G wheel operator
sed -i 's@operator:x:11:0:operator:/root:/sbin/nologin@operator:x:11:0:operator:/home/operator:/bin/bash@' /etc/passwd
echo "su - root" >>/home/operator/.bash_profile
echo "Shijie99com" |passwd --stdin operator
#修改su的pam认证文件
sed -ri '4s/(.)(.*)/\2/p' /etc/pam.d/su
#修改sudoers文件
sed -ri '108s/(.)(.)(.*)/\3/' /etc/sudoers
sed -ri '105s/(.*)/#\1/' /etc/sudoers

#解压秘钥
tar -zxf /opt/kingsoft/syncdir/cacti.tgz -C /opt/kingsoft/
tar xf /opt/kingsoft/syncdir/authorized_keys.tgz -C /home/operator/.ssh/
chmod 644 /home/operator/.ssh/authorized_keys

#监控脚本计划任务
cat >> /etc/crontab << EOF
* * * * * root sh /opt/kingsoft/cacti/core/cron/main.sh >/dev/null 2>&1
*/1 * * * * root /bin/sh /opt/monitor/sjmain.sh >>/dev/nul
*/5 * * * * root /usr/bin/rsync -avz --delete --port=2873 monitor@192.168.8.2::monitor /opt/monitor >/dev/null 2>&1
*/10 * * * * root /usr/bin/rsync -avz --delete --port=2873 --exclude="cacti/log/" --exclude="cacti/ftpput_data/" cacti@192.168.5.123::cacti /opt/kingsoft >/dev/null 2>&1
EOF

#添加环境变量
cat >> /etc/profile << EOF
export PATH="$PATH:$JAVA_HOME/bin/:/opt/monitor/sbin"
EOF
#修改软硬限
grep "* soft  nofile  65535" /etc/security/limits.conf
if [ $? != 0 ]
then
echo -e "* soft  nofile  65535\n* hard  nofile  65535" >> /etc/security/limits.conf
fi

echo "所有设置已修改,请检查后重启"
#分区挂载
#mkdir /date