import time
def readMemInfo():
    res = {
    'total':0, 'free':0, 'buffers':0, 'cached':0
    }
    f = open('/proc/meminfo')
    lines = f.readlines()
    f.close()
    i = 0
    for line in lines:
        if i == 4:
            break
        line = line.lstrip()
        memItem = line.lower().split()
        if memItem[0] == 'memtotal:':
            res['total'] = long(memItem[1])
            i = i +1
            continue
        elif memItem[0] == 'memfree:':
            res['free'] = long(memItem[1])
            i = i +1
            continue
        elif memItem[0] == 'buffers:':
            res['buffers'] = long(memItem[1])
            i = i +1
            continue
        elif memItem[0] == 'cached:':
            res['cached'] = long(memItem[1])
            i = i +1
            continue
    return res
 
def calcMemUsage(counters):
    used = counters['total'] - counters['free'] - counters['buffers'] - counters['cached']
    total = counters['total']
    remain=counters['free'] + counters['buffers'] + counters['cached']
    return used*100/total
 
if __name__ == '__main__':
    while(True):
        counters = readMemInfo()
        print calcMemUsage(counters)
        time.sleep(1)