# -*- coding: utf-8 -*
'''
定时任务：每天凌晨更新当天打过的电话线索，判断线索是否删除、修改、添加
'''

import sys
sys.path.append("../")

from conn_sql import conn_only_xddb

def remove_timer():
    conn_only = conn_only_xddb()
    cur_only = conn_only.cursor()
    cur_only.execute("select Cellphone,Company,Last_Action from crm_t_call_action ")
    for row in cur_only.fetchall():
        cellphone = row[0]
        company_name = row[1]
        last_action = row[2]
        process_clue(cellphone, company_name, last_action)


def process_clue(cellphone,company_name,last_action):
    print()

if __name__ == '__main__':
    pass