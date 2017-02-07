#!/usr/bin/env bash
#============================== 用途 =================================
#
# 压缩日志，需手动更改关键字："catalina.2016"
#============================== config =================================
loglist=$(ls | grep catalina.2016 | grep -v tgz)



#==============================function=================================
function tar_log() {
for logs in ${loglist}
do
tar -zcvf ${logs}.tgz ${logs} --remove-files
done
}


#==============================main=================================
tar_log
exit 0;