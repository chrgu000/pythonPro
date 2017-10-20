# -*- coding: utf-8 -*
'''
定时任务：每天晚上零点更新当天的数据
    将每天打过的记录对应到线索的id
'''

from threading import Timer
from plan_customer_alter import add_clue_id
from datetime import timedelta
from datetime import datetime
import time

def plan_customer_timer():
    dead_time = str(datetime.now() - timedelta(days=1))
    print(dead_time)
    add_clue_id(dead_time)
    t = Timer(24*3600, plan_customer_timer)
    t.start()

if __name__ == '__main__':
    time.sleep(9*3600)
    plan_customer_timer()
    pass