#!/usr/bin/env bash
#==============================config=================================
server_path='/data/opt'
tomcatfile=$(ls "${server_path}" |grep tomcat |grep -v tar.gz | grep -v tgz | grep -v tar | grep -v bak$| xargs)
jbossfile=$(ls "${server_path}" |grep jboss |grep -v tar.gz | grep -v tgz | grep -v tar | grep -v bak$| xargs)

#==============================function=================================
function gettomcatinfo(){
for file in ${tomcatfile}
do
    port=$(cat "${server_path}"/"${file}"/conf/server.xml |grep "\<Connector.*protocol=\"HTTP\/1.1" | awk '{print $2}'| awk -F"\"" '{print $2}')
    packages=$(ls "${server_path}"/"${file}"/webapps/ | grep .*war$ | xargs)
    if [ -f "${server_path}"/"${file}"/README.txt ];then
        usage=$(grep \<shijie99\> "${server_path}"/"${file}"/README.txt | awk -F">" '{print $2}'| xargs)
    else
        usage=""
    fi
    if [ -n ${port} ];then

        echo -e "${file} \t${port} \t${packages} \t${usage}" >> ${server_path}/serverfile.txt

    fi
done
}

function getjbossinfo(){
for file in ${jbossfile}
do
    port1=$(cat "${server_path}"/"${file}"/standalone/configuration/standalone.xml | grep port-offset: |awk -F"}" '{print $1}' | awk -F":" '{print $2}')
    port2=$(cat "${server_path}"/"${file}"/standalone/configuration/standalone.xml | grep "socket-binding name=\"http\"" | awk -F"\"" '{print $4}')
    port=$[${port1}+${port2}]
    packages=$(ls "${server_path}"/"${file}"/standalone/deployments/ | grep .*war$ | xargs)
    if [ -f "${server_path}"/"${file}"/README.txt ];then
        usage=$(grep \<shijie99\> "${server_path}"/"${file}"/README.txt | awk -F">" '{print $2}'| xargs)
    else
        usage=""
    fi
    if [ -n ${port} ];then
        echo -e "${file}   \t${port} \t${packages} \t${usage}" >> ${server_path}/serverfile.txt
    fi
done
}


#==============================main=================================
> ${server_path}/serverfile.txt
gettomcatinfo
getjbossinfo