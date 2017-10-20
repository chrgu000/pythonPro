# -*- coding: utf-8 -*
'''
定时任务，有效性评分，每天更新
'''
import time
from threading import Timer
import sys

sys.path.append("../")
from validity_score import get_validity

def func():
    print("score start time:" + str(time.time()))
    get_validity()
    print("score end time:" + str(time.time()))
    t=Timer(24*3600,func)
    t.start()

if __name__ == "__main__":
    time.sleep(8*3600)
    func()
