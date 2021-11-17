#!/usr/bin/python3
#TODO
#adding expire-time setting in ini

import psutil
import sys, os
import time as t
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import daemon_class
from configparser import ConfigParser
sys.path.insert(1, '/home/nls/py/pytools')
import nls_util as nut
'''
this daemon is not ready for use, yet
'''

class Batd(daemon_class.Daemon):
    def __init__(self, pidfile, ini_file = "batd.ini"):
        super().__init__(pidfile)
        self.ini_file = ini_file
        if not os.path.exists(self.ini_file):
            os.system(f"touch {self.ini_file}")
            print("initialized ini-file")
        self.ini = ConfigParser()
        self.ini.read(self.ini_file)
        self.parse_ini()
        self.log_file = self.ini["batd"]["log_file"]
        if not os.path.exists(self.log_file):
            os.system(f"touch {self.log_file}")

    def run(self):
        jinterval = 5
        it = 0
        self.parse_ini()
        cf = self.ini["batd"]
        while True:
            it += 1
            try:
                t.sleep(int(cf["scan_rate"]))
            except:
                print("scan_rate must be an integer")
                t.sleep(int(self.standard_cft["scan_rate"]))

            #these standard values just take place when values in ini are not appropriate
            #nf, nt bwt, bct = 2, 1, 70, 10
            nf, nt, bwt, bct = int(cf["notify_factor"]), int(cf["notify_time_ms"]), int(cf["battery_warn_trashhold"]), int(cf["battery_critical_trashhold"])

            battery_percent = psutil.sensors_battery().percent
            date = dt.now().strftime("%d-%m_%H:%M")
            #log = f"{battery_percent:.2f},{date=},{it=}, {nf=}, {nt=}, {bwt=},{bct=}\n"
            log = f"{battery_percent:.2f},{date}\n"
            with open(self.log_file, "a") as f:
                f.write(log)

            if int(battery_percent) < bwt:
                if it % nf:
                    nut.notify("batd", f"{battery_percent}", " --urgency=critical " if battery_percent <= bct else "")
            
    def parse_ini(self):
        self.standard_cft = {
        #       name        |   standard value
                "scan_rate":        "5"
                ,"notify_factor":   "10"
                ,"notify_time_ms":  "1"
                ,"log_file":        "/tmp/batd.csv"
                ,"battery_warn_trashhold": "50"
                ,"battery_critical_trashhold": "20"
                }
        write_flg = False
        if "batd" not in self.ini:
            self.ini.add_section("batd")
            write_flg = True
        for cfg in self.standard_cft:
            if cfg not in self.ini["batd"]:
                self.ini["batd"][cfg] = self.standard_cft[cfg]
                write_flg = True

        if write_flg:
            self.ini.write(open(self.ini_file, "w"))

    def check_ini(self):
        #check ini for correctness (ints are ints)
        pass

    def cat_log(self):
        os.system(f"cat {self.log_file}")

    def clean(self):
        self.clean_ini()
        self.clean_log()
    def clean_ini(self):
        os.system(f"rm {self.ini_file}")
    def clean_log(self):
        os.system(f"rm {self.log_file}")

    def pd_(self):
        df = pd.read_csv(self.log_file, index_col=1, names=["bat", "date"], parse_dates=True)
        df.plot()
        print(df)
        if input("[s]how plot\n>") == "s":plt.show()

    def query(self):
        os.system("bat")
#if __name__ == "__main__"
batd = Batd('/tmp/batd.pid')
options = {"start":     batd.start 
        ,"stop":        batd.stop 
        ,"restart":     batd.restart 
        ,"log":         batd.cat_log
        ,"ini":         batd.parse_ini
        ,"clean":       batd.clean
        ,"cleanlog":    batd.clean_log
        ,"cleanini":    batd.clean_ini
        ,"pd":          batd.pd_
        ,"query":       batd.query
        }

def usage_die(false_arg = ""):
    print(nut.cli["BOLD"]) 
    if false_arg != "":print(f"no argument named {false_arg} ...")
    print(f"usage : {sys.argv[0]} ", end="")
    for opt in options: print(opt, end='|')
    print(nut.cli["RESET"])

if len(sys.argv) >= 2:
    for arg in sys.argv[1:]:
        if arg in options:
            print(f"exec: {sys.argv[0]} {arg=}")
            options[arg]()
        else: usage_die(arg)
else:
    usage_die()

