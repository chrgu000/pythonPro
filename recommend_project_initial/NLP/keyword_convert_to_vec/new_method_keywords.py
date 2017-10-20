# -*- coding: utf-8 -*
import numpy as np
from numpy import *
import math
def new_extract_keywords():
    file = open("param8.csv", errors='ignore')
    all_lines = file.readlines()


def get_all_character():
    character_dict={}
    file = open("param8.csv", errors='ignore')
    all_lines = file.readlines()
    for i in range(0,len(all_lines)):
        line_list=set(all_lines[i])
        for j in range(0,len(line_list)):
            print()
            # if line_list[j]


if __name__=='__main__':
    str1="技术服务销售服装服饰鞋帽皮具电子产品针纺织品箱包皮具皮革制品玻璃制品塑料制品"
    str2="电子设备的研发生产和销售电子产品"
    character=[]
    for s in set(str1):
        if s not in character:character.append(s)
    for s in set(str2):
        if s not in character:character.append(s)
    list_1=[]
    list_2=[]
    for i in range(0,len(character)):
        if character[i] in set(str1):
            list_1.append(1)
        else:
            list_1.append(0)
    for i in range(0, len(character)):
        if character[i] in set(str2):
            list_2.append(1)
        else:
            list_2.append(0)
    a1=array(list_1)
    a2=array(list_2)
    arr=zeros((len(character),len(character)))
    l1=[]
    l1=list(set(str1))
    for s in l1:
        if s in l1:
            index_c=l1.index(s)
            for ss in l1:
                index_i=l1.index(ss)
                arr[index_c,index_i]=(math.fabs(index_i-index_c))/len(character)
    l2 = []
    l2 = list(set(str2))
    for s in l2:
        if s in l2:
            index_c=l2.index(s)
            for ss in l2:
                index_i=l2.index(ss)
                arr[index_c,index_i]=(math.fabs(index_i-index_c))/len(character)

    print(arr)
    pass