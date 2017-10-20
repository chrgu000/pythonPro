# -*- coding: utf-8 -*
import numpy as np
def get_location():
    file = open("qthl.txt", encoding='utf8', errors='ignore')
    lines = file.readlines()
    for i in range(0,10):
        addr=lines[i].split("	")[7]
        print(addr)


if __name__ == '__main__':
    # get_location()

    # 删除矩阵某个列
    array = ([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(array)
    aa=np.delete(array,[0,1],axis=1)
    print(aa)
    pass