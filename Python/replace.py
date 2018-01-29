# _*_ coding:utf-8 _*_
# auth: xuyong
# used: 替换admincs项目下所有符合条件的域名
# help：admincs.py fz|online
import os
import sys


def getallfile(path):
    allfile = []
    allfilelist = os.listdir(path)
    for file in allfilelist:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            getallfile(filepath)
        else:
            allfile.append(filepath)
    return allfile


def modifyfile(filelist, platform='www', indexurl='None', fileurl='None'):
    indexurl = indexurl
    fileirl = fileurl
    resultdic = {}
    for file in filelist:
        num = 0
        with open(file, 'r') as f:
            lines = f.readlines()
            with open(file, 'w') as w:
                for i in lines:
                    if platform == 'www':
                        if i != i.replace('test.online.gintong.com', indexurl):
                            num += 1
                        w.write(i.replace('test.online.gintong.com', indexurl))
                    elif platform == 'file':
                        if i != i.replace('file.online.gintong.com', fileurl):
                            num += 1
                        w.write(i.replace('file.online.gintong.com', fileurl))
                    else:
                        return 'Error'
    return resultdic

if __name__ == '__main__':
    pl = sys.argv[1]
    if pl == 'fz':
        indexurl = "fzwww.gintong.com"
        fileurl = "fzfile.gintong.com"
    elif pl == 'online':
        indexurl = "www.gintong.com"
        fileurl = "file.gintong.com"
    else:
        sys.exit()
    path = "/webserver/webdata/admincs"
    filelist = getallfile(path)
    wwwnum = modifyfile(filelist, type='www', indexurl=indexurl)
    filenum = modifyfile(filelist, type='file', fileurl=fileurl)
    www = 0
    for value in wwwnum.values():
        www += int(value)
    print("www { %d } files changed { %d } items." % (len(wwwnum), www))
    file = 0
    for value in filenum.values():
        file += int(value)
    print("file { %d } files changed{ %d } items." % (len(filenum), file))