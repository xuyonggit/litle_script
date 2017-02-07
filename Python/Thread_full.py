# 用途：
# 死循环创建线程。直至卡死

import threading
from time import sleep


def task():
    print()
    sleep(6000)


while True:
    t = threading.Thread(target=task)
    t.setDaemon(True)
    t.start()