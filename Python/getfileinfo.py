#!/bin/env python3
# -*- coding: utf-8 -*-
"""
desc : linux系统下获取目录下文件详情：创建者，创建时间，最新修改时间
usages: getfileinfo         操作当前目录
        getfileinfo /tmp/tmp    操作指定目录（绝对路程
        getfileinfo tmp     操作指定目录（相对路径）
author: xuyong
"""
import os
import datetime
import pwd
import sys


class FileInfo:
    def __init__(self, filepath=''):
        if not filepath:
            filepath = os.getcwd()
        self.filepath = filepath

    def _getFile(self):
        """
        获取文件列表
        :return: 文件列表
        """
        filelist = []
        files = os.listdir(self.filepath)
        for i in range(len(files)):
            path = os.path.join(self.filepath, files[i])
            if os.path.isfile(path):
                filelist.append(files[i])
        return filelist

    def getInfo(self):
        filelist = self._getFile()
        for i in range(len(filelist)):
            # 文件绝对路径
            file_p = os.path.join(self.filepath, filelist[i])
            if os.path.isdir(file_p):
                continue
            stat = os.stat(file_p)
            uid = stat.st_uid
            username = pwd.getpwuid(uid).pw_name
            # 获取创建时间
            ctime = os.path.getctime(file_p)
            datectime = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M')
            # 获取修改时间
            mtime = os.path.getmtime(file_p)
            datemtime = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
            print(username, datectime, datemtime, filelist[i])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        filepath = os.getcwd()
    else:
        path = sys.argv[1]
        if len(path.split(os.path.sep)) > 1:
            if os.path.exists(path):
                filepath = sys.argv[1]
        else:
            if os.path.exists(os.path.join(os.getcwd(), path)):
                filepath = os.path.join(os.getcwd(), path)
            else:
                raise FileNotFoundError
    if filepath:
        Main = FileInfo(filepath)
        Main.getInfo()
