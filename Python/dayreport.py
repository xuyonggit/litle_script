# _*_ coding:utf-8 _*_
from datetime import datetime
import os


def check_today(list):
    for i in list:
        L3.append(i['date'])
        if day_date not in L3:
            return False
        else:
            return True


# 插入工作内容
def insert_new():
    for i in L2:
        # 今日插入新内容
        if check_today(L2) == True:
            if i['date'] == day_date:
                x = i['info']
                num = len(x) + 1
                x.append('%d、%s；' % (num, workinfo))
                # 重新写入文件
                os.remove(filename)
                with open(filename, 'w') as f:
                    for i in L2:
                        f.write(u"时间: %s\n" % i['date'])
                        f.write(u"职位: %s\n" % i['zhiwei'])
                        f.write(u"工作内容:\n")
                        for info in i['info']:
                            f.write('%s\n' % info)
                        f.write(day_split + '\n')
        else:
            # 创建今日模板
            D4 = {'date': day_date, 'zhiwei': u'运维工程师', 'info' : ['1、%s；' % workinfo]}
            L2.insert(0, D4)
            # 重新写入文件
            os.remove(filename)
            with open(filename, 'w') as f:
                for i in L2:
                    f.write(u"时间: %s\n" % i['date'])
                    f.write(u"职位: %s\n" % i['zhiwei'])
                    f.write(u"工作内容:\n")
                    for info in i['info']:
                        f.write('%s\n' % info)
                    f.write(day_split + '\n')

if __name__ == '__main__':
    # Template
    day_split = "=================================="
    day_date = datetime.today().strftime("%Y-%m-%d")
    zhiwei = "运维工程师"
    workinfo = input("Please input work info: ")


    # define list
    check_list = []
    L1 = []
    L2 = []
    L3 = []

    filename = 'report.txt'
    with open(filename, 'r+') as f:
        for i in f.readlines():
            check_list.append(''.join(i).strip('\n'))
        if len(check_list) == 0:
            f.write(u"时间: %s\n" % day_date)
            f.write(u"职位: %s\n" % zhiwei)
            f.write(u"工作内容:\n")
            f.write('1、%s；\n' % workinfo)
            f.write(day_split + '\n')
            exit(0)
        else:
            for j in check_list:
                if j != day_split:
                    L1.append(j)
                else:
                    info_dict = {}
                    info_dict['date'] = L1[0][4:]
                    info_dict['zhiwei'] = L1[1][4:]
                    del L1[0:3]
                    info_dict['info'] = L1
                    L2.append(info_dict)
                    L1 = []

    insert_new()