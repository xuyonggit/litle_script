# _*_ coding:utf-8 _*_
import random


# 字符菜单
# 获取指定数量数字,返回列表
def get_num(num=1):
    templates = "0123456789"
    return random.sample(templates, num)


# 获取指定数量小写字母,返回列表
def get_lword(num=1):
    L = []
    for i in range(97, 123):
        L.append(chr(i))
    return random.sample(L, num)


# 获取指定数量大写字母,返回列表
def get_bword(num=1):
    L = []
    for i in range(65, 91):
        L.append(chr(i))
    return random.sample(L, num)


# 获取指定数量特殊符号,返回列表
def get_fuhao(num=1):
    S = "!~`@#$%^&*()_+}{[]:;?/>.<,|"
    return random.sample(S, num)


class main():
    def __init__(self, level=2):
        self.level = level
        self.passwd = ""

    # 级别1(8位)
    def level1(self, num=8):
        self.passwd = ""
        # 1/2 数字 & 1/2 小写字母 & other 小写字母
        nums = num // 2
        lw = num // 2
        other = num % 2
        listofpasswd = get_num(nums) + get_lword(lw) + get_lword(other)
        temp_l = [x for x in range(0, len(listofpasswd))]
        while len(temp_l) > 0:
            l = random.sample(temp_l, 1)
            self.passwd = self.passwd + str(listofpasswd[l[0]])
            temp_l.remove(l[0])
        return self.passwd

    # 级别2（12位）
    def level2(self, num=12):
        self.passwd = ""
        # 1/3 数字 & 1/3 小写字母 & 1/3 大写字母  & other 小写字母
        nums = num // 3
        lw = num // 3
        bw = num // 3
        other = num % 3
        listofpasswd = get_num(nums) + get_lword(lw) + get_bword(bw) + get_lword(other)
        temp_l = [x for x in range(0, len(listofpasswd))]
        while len(temp_l) > 0:
            l = random.sample(temp_l, 1)
            self.passwd = self.passwd + str(listofpasswd[l[0]])
            temp_l.remove(l[0])
        return self.passwd

    # 级别3（18位）
    def level3(self, num=18):
        self.passwd = ""
        # 1/5 数字 & 1/5 小写字母 & 1/5 大写字母 1/5 特殊符号 & other 小写字母
        nums = num // 5
        lw = num // 5
        bw = num // 5
        fh = num // 5
        other = num % 5
        listofpasswd = get_num(nums) + get_lword(lw) + get_bword(bw) + get_fuhao(fh) + get_lword(other)
        temp_l = [x for x in range(0, len(listofpasswd))]
        while len(temp_l) > 0:
            l = random.sample(temp_l, 1)
            self.passwd = self.passwd + str(listofpasswd[l[0]])
            temp_l.remove(l[0])
        return self.passwd


if __name__ == '__main__':
    C = main()
    print("level1: {}".format(C.level1()))
    print("level2: {}".format(C.level2()))
    print("level3: {}".format(C.level3()))