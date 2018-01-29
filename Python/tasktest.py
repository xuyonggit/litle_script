# -*- coding:utf-8 -*-
# 定时器实例
import sched
import time
schedule = sched.scheduler(time.time, time.sleep)


def func(inc=5):
    print("定时器执行......")
    schedule.enter(inc, 0, func)
    schedule.run()

if __name__ == '__main__':
    func(6)