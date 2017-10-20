# -*- coding: utf-8 -*

import time
from threading import Timer
import sys

sys.path.append("../")
from positive_sets import update_record_clue
def func():
    print("sets start time:"+str(time.time()))
    update_record_clue()
    print("sets end time:" + str(time.time()))
    t=Timer(24*3600,func)
    t.start()


if __name__ == "__main__":
    time.sleep(12*3600)
    func()
