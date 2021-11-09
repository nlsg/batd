#!/usr/bin/env python
import psutil
import sys, os
import time as t
from datetime import datetime as dt
import nls_util as nut
import pandas as pd
import matplotlib.pyplot as plt
import daemon_class
from configparser import ConfigParser
'''
this daemon is not ready for use, yet
'''

class Batd(daemon_class.Daemon):
    def __init__(self, pidfile, log_file = "/tmp/batd.csv", csv_file = "/tmp/batd.csv", ini_file = "batd.ini"):
        super().__init__(pidfile)
        self.log_file = log_file
        self.csv_file = csv_file
        self.ini_file = ini_file

    def run(self):
        interval = 5 #5 * 60
        it = 0
        while True:
            t.sleep(interval)
            battery_percent = psutil.sensors_battery().percent
            date = dt.now().strftime("%d-%b_%H-%M")
            log = f"{battery_percent:.2f},{date},{(it:= it + 1)}\n"
            with open(self.log_file, "a") as f:
                f.write(log)
            if it % 2:
                os.system(f"notify-send \"batd\" \"it: {it}\"")

    def info(self):
        print(f"info printed: {it}\n")

    def cat_log(self):
        os.system(f"cat {self.log_file}")

    def clean(self):
        os.system(f"rm {self.log_file}")

    def pd_(self):
        df = pd.read_csv(self.csv_file)
        df.plot()
        plt.show()

    def fetch_ini(self):
        os.system(f"rm {self.ini_file}")
        cfg = ConfigParser()
        cfg.add_section("sec")
        cfg.set("sec","opt1","1")
        cfg.write(open(self.ini_file, "w"))
        print(type(cfg["sec"]["opt1"]))

if __name__ == "__main__":
    batd = Batd('/tmp/batd.pid')
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            batd.start()
        elif "stop" == sys.argv[1]:
            batd.stop()
        elif "restart" == sys.argv[1]:
            batd.restart()
        elif "info" == sys.argv[1]:
            batd.info()
        elif "log" == sys.argv[1]:
            batd.cat_log()
        elif "clean" == sys.argv[1]:
            batd.clean()
        elif "pd" == sys.argv[1]:
            batd.pd_()
        elif "ini" == sys.argv[1]:
            batd.fetch_ini()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
