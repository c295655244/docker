import time


class get_cpu():

    def readCpuInfo(self):
        f = open('/proc/stat')
        lines = f.readlines()
        f.close()
        line = lines[0].lstrip()
        counters = line.split()
        total = 0
        for i in xrange(1, len(counters)):
            total = total + long(counters[i])
        idle = long(counters[4])
        return {
            'total': total, 'idle': idle
        }

    def calcCpuUsage(self, counters1, counters2):
        idle = counters2['idle'] - counters1['idle']
        total = counters2['total'] - counters1['total']
        return 100 - (idle*100.0/total)

    def getcpu(self):
        while(True):
            counters1 = self.readCpuInfo()
            time.sleep(1)
            counters2 = self.readCpuInfo()
            result = str(self.calcCpuUsage(counters1, counters2))
            print result


cpu = get_cpu()
cpu.getcpu()
