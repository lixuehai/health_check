import psutil
import os
def load_stat():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    print("1 min loadavg :%s, 5 min loadavg: %s" %(loadavg['lavg_1'],loadavg['lavg_5']))

def getCPUState(interval=1):
    cpuPercent = psutil.cpu_percent(interval)
    print("Logic CPU Usage rate: %s%%" % str(cpuPercent))

def getMemorystate():
    phymem = psutil.virtual_memory()
    buffers = getattr(psutil, 'phymem.buffers', lambda: 0)()
    cached = getattr(psutil, 'phymem.cached', lambda: 0)()
    used = phymem.total - (phymem.free + buffers + cached)
    line = "Memory usage rate:%5s%% Used mem:%6s Total mem:%s" % (
        phymem.percent,
        str(int(used / 1024 / 1024)) + "M",
        str(int(phymem.total / 1024 / 1024)) + "M"  )
    if phymem.percent > 90:
        print("Memory utilization greater than 90%" )
    else:
        print(line)



if __name__ == "__main__":
   getCPUState(0.1)
   load_stat()
   getMemorystate()

