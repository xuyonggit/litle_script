# _*_ coding: utf-8 _*_
import random


def makedata(List):
    m = 0
    while m < len(List):
        for i in range(0, len(List)):
            if i != len(List) - 1:
                if List[i] >= List[i+1]:
                    List[i], List[i+1] = List[i+1], List[i]
        m += 1
    return List


if __name__ == '__main__':
    List1 = []
    num = 0
    while num < 10:
        List1.append(random.randint(0, 100))
        num += 1
    print(List1)
    a = makedata(List1)
    print(a)