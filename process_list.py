import os
import psutil
import time
from globaldata import *

logPath = DATA_DIR + "process_log\\"
if not os.path.exists(logPath):
    os.mkdir(logPath)

separator = "-" * 80
format = "%5s: %30s  %12s %12s %7s %s"
format2 = "%5s: %30s  %12s %12s %9.2f %s"
run_count = 0
while run_count < 2:
    procs = psutil.process_iter()
    procs = sorted(procs, key=lambda proc: proc.name())

    for proc in procs:
        pid = proc.pid
        name = proc.name()[:-4]
        rss, vms = proc.memory_info()[:2]
        rss = str(rss)
        vms = str(vms)
        cpu_pct = proc.cpu_percent()
        try:
            exe = proc.exe()
        except:
            exe = "System"

        if int(cpu_pct) > 0:
            print format2 % (pid, name, vms, rss, cpu_pct, exe)
    if run_count == 0:
        print 'initial run complete'
    time.sleep(10)
    run_count += 1
