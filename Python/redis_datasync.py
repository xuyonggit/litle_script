#!/usr/bin/env python3
# auther: xuyong
# desc: redis数据迁移至redis集群

import redis
from rediscluster import StrictRedisCluster
import sys

redis_conf = {
    'host': '10.10.22.114',
    'port': 6379
}
redis_nodes = [
    {'host':'10.10.22.114','port':6370},
    {'host':'10.10.22.114','port': 6371},
    {'host':'10.10.22.114','port': 6372},
    {'host':'10.10.22.114','port': 6373},
    {'host':'10.10.22.114','port': 6374},
    {'host':'10.10.22.114','port': 6375}
]
def getSessionKeys():
    l1 = []
    redis_pool = redis.ConnectionPool(**redis_conf)
    r = redis.Redis(connection_pool=redis_pool)
    data = r.keys("user:sessionId*")
    for key in data:
        dic1 = {}
        dic1[key.decode()] = r.get(key.decode())
        l1.append(dic1)
    return l1

def writeNewRedisCluster(datalist=[]):
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception as e:
        print("connection Failed")
        sys.exit(1)
    for d in datalist:
        for key,value in d.items():
            redisconn.set(key, value)

def readNewRedisCluster():
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception as e:
        print("connection Failed")
        sys.exit(1)
    data = redisconn.keys("user:sessionId*")
    print(len(data),data)

if __name__ == '__main__':
    #writeNewRedisCluster(getSessionKeys())
    readNewRedisCluster()
