# _*_ coding:utf-8 _*_
import random


# 字符菜单
# 获取指定数量数字
def get_num(num=1):
    templates = "0123456789"
    return random.sample(templates, num)


# 获取指定数量小写字母
def get_lword(num=1):
    L = []
    for i in range(97, 123):
        L.append(chr(i))
    return random.sample(L, num)


# 获取指定数量大写字母
def get_bword(num=1):
    L = []
    for i in range(65, 91):
        L.append(chr(i))
    return random.sample(L, num)


# 获取指定数量特殊符号
def get_other(num=1):
    S = "!~`@#$%^&*()_+}{[]:;?/>.<,|"
    return random.sample(S, num)


class main():
    def __init__(self, level=2):
        self.level = level
        self.passwd = ""

    def level1(self, num=8):
        # 1/2 数字 & 1/2 小写字母 & other 小写字母
        nums = num // 2
        lw = num // 2
        other = num % 2
        listofpasswd = get_num(nums) + get_lword(lw) + get_lword(other)
        temp_l = [x  for x in range(0, len(listofpasswd))]
        while len(temp_l) > 0:
            l = random.sample(temp_l, 1)
            self.passwd = self.passwd + str(listofpasswd[l[0]])
            temp_l.remove(l[0])
        return self.passwd

if __name__ == '__main__':
    C = main()
    print(C.level1(9))