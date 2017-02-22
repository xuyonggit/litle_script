# _*_coding:utf-8_*_
# x = 1  2  3  5  8 ...
# n = 1  2  3  4  5 ...
# 给出n的值自动返回对应x的值


def func1(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        x = func1(n - 1) + func1(n - 2)
        return x

# test
for i in range(1, 10):
    print("-->当n的值为: %d  x值为：%d" % (i, func1(i)))

