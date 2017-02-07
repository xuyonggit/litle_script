#!/usr/bin/env bash
# 用途：
# Linux系统用于添加，删除用户脚本
# 使用方法：
# 运行：gguser add/del 用户名
#==============================config=================================
rsa_path='/data/worken/operator/rsafile'

#==============================function=================================
function fhelp(){
echo """Usage:
        gguser [add/del] username
"""
}

function add(){
if [ -z $1 ];then
    fhelp
    exit 0
else
    useradd -G wheel $1
    echo "${1}99" | passwd --stdin ${1} >>/dev/null
    mkdir /home/${1}/.ssh && ssh-keygen -t rsa -P "" -f /home/${1}/.ssh/id_rsa >> /dev/null
    mv /home/${1}/.ssh/id_rsa.pub /home/${1}/.ssh/authorized_keys
    mv /home/${1}/.ssh/id_rsa ${rsa_path}/${1}.rsa
    sed -i '$aAllowUsers  '${1}'' /etc/ssh/sshd_config
    systemctl restart sshd
    keyinfo=`cat ${rsa_path}/${1}.rsa`

fi
echo -e """==========info==========
new user: ${1}
password: ${1}99
key path: ${rsa_path}
key name: ${1}.rsa
key info:
${keyinfo}
==========END==========
"""
}

function del(){
if [ -z $1 ];then
    fhelp
    exit 0
else
    userdel -r $1
    rm -rf ${rsa_path}/${1}.rsa
    sed -i '/^AllowUsers  '${1}'/d' /etc/ssh/sshd_config
    systemctl restart sshd
fi
}

#==============================main=================================
case $1 in
add)add $2;;
del)del $2;;
*)fhelp;;
esac