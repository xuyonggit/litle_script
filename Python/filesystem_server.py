# -*- coding: utf-8 -*-
import os
import pymysql
import threading


class operator(object):
    def __init__(self, filepaths=[]):
        self.filepaths = filepaths
        self.datalist = []
        self.getFileList()

    def Dbcon(self):
        return pymysql.connect(
            host='mysql.local.com',
            port=3306,
            user='u_filesystem',
            password='Gintong.com',
            db='yunwei',
            charset='utf8mb4',
            autocommit=True
        )

    def getFile(self, filepath):
        """
        截取文件类型，返回目录类型列表
        :param filepath:
        :return:
        """
        for fileanddir in os.listdir(filepath):
            now_path = filepath
            v1_list = []
            if os.path.isfile(os.path.join(now_path, fileanddir)):
                self.datalist.append((fileanddir, '/'.join((now_path, fileanddir))))
            else:
                v1_list.append(os.path.join(filepath, fileanddir))
        return v1_list

    def getFileList(self):
        # 递归获取目录下各级文件
        checks = self.filepaths
        while len(checks) > 0:
            for fp in checks:
                checks += self.getFile(fp)
                checks.remove(fp)

    def upDateDb(self):
        """
        更新数据库数据，变动则更新，不存在则写入，否则pass
        :return:
        """
        conn = self.Dbcon()
        try:
            with conn.cursor() as Cur:
                for filename, path_uri in self.datalist:
                    Cur.execute("select * from tb_file_detail where filename='{}'".format(filename))
                    result = Cur.fetchone()
                    if not result:
                        Cur.execute("INSERT INTO tb_file_detail (`filename`, `download_url`) VALUES ('{}', '{}')".format(filename, path_uri))
                    elif result[2] != path_uri:
                        Cur.execute("UPDATE tb_file_detail SET `download_url`='{}' where `filename`='{}';".format(path_uri, filename))
        finally:
            conn.close()

    def clearData(self):
        """
        清理mysql 多余数据
        :return:
        """
        dirdata = [x[0] for x in self.datalist]
        conn = self.Dbcon()
        try:
            with conn.cursor() as Cur:
                if len(dirdata) > 0:
                    if len(dirdata) == 1:
                        Cur.execute("SELECT `id` from tb_file_detail WHERE `filename`={}".format(dirdata[0]))
                    else:
                        Cur.execute("SELECT `id` from tb_file_detail WHERE `filename` NOT IN {}".format(tuple(dirdata)))
                    NOUSEID = [id[0] for id in Cur]
                    if len(NOUSEID) > 0:
                        if len(NOUSEID) == 1:
                            Cur.execute("DELETE FROM tb_file_detail WHERE `id`={};".format(NOUSEID[0]))
                        else:
                            Cur.execute("DELETE FROM tb_file_detail WHERE `id` in {};".format(tuple(NOUSEID)))
        finally:
            conn.close()


if __name__ == '__main__':
    def func1(time):
        global FILEPATHLIST
        FILEPATHLIST = ['count_nginx', 'qt_dir']
        print("定时任务启动。。。。。。")
        M = operator(FILEPATHLIST)
        print("更新数据库：{}".format([filename[0] for filename in M.datalist]))
        M.upDateDb()
        print("数据库更新完成，开始清理垃圾数据。。。")
        M.clearData()
        print("任务结束。")
        global timer
        timer = threading.Timer(time, func1, args=[time])
        timer.start()
    func1(10)
