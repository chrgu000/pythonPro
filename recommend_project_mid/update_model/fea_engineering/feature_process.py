# -*- coding: utf-8 -*
'''
sql()
feature_pro():给出特征表中的数据，对每一个特征再处理
'''
import numpy as np

def sql():
    return "select c_type,c_has_site,c_employees_min,c_employees_mean,c_employees_max,c_reg_capital,c_reg_date,c_reg_address,c_tyc_score,c_tyc_summary,p_major,c_reg_address_lon,c_reg_address_lat,c_tfidf_vec,Clue_Id from clue_feature "

def feature_pro(row):
    is_insert = True
    sample = np.zeros(70000)
    # sample = np.zeros(357)
    # 公司类型
    try:
        sample[0] = row[0]
    except Exception as e:
        is_insert=False

    # 是否有网站
    try:
        sample[1] = row[1]
    except Exception as e:
        is_insert=False

    # 公司员工最小值
    try:
        sample[2] = row[2]
    except Exception as e:
        is_insert=False

    # 公司员工均值
    try:
        sample[3] = row[3]
    except Exception as e:
        is_insert=False

    # 公司员工最大值
    try:
        sample[4] = row[4]
    except Exception as e:
        is_insert=False

    # 注册资金
    try:
        sample[5] = row[5]
    except Exception as e:
        is_insert=False

    # 注册日期
    try:
        sample[6] = row[6]
    except Exception as e:
        is_insert=False

    # 地区做onehot处理
    if row[7] != 0 or len(str(row[7])) > 5:
        try:
            sample[7+int(str(row[7])[0:2])] = 1
            sample[7+100+int(str(row[7])[2:4])] = 1
            sample[7+100+100+int(str(row[7])[4:6])] = 1
        except Exception as e:
            is_insert = False


    # 天眼评分
    try:
        sample[308] = row[8]
    except Exception as e:
        is_insert=False

    # 天眼概览
    try:
        if len(str(row[9])) > 3:
            summery_dict = eval(row[9])
            for k,v in summery_dict.items():
                sample[309+int(k)] = v
    except Exception as e:
        is_insert = False

    # 职位
    try:
        sample[354] = row[10]
    except Exception as e:
        is_insert = False

    # 经纬度
    try:
        sample[355] = row[11]
        sample[356] = row[12]
    except Exception as e:
        is_insert = False

    # 文本向量
    try:
        if row[13] != -1 and ";" not in row[13]:
            k_list = row[13].split(",")
            for i in range(0,len(k_list)-1):
                index = int(k_list[i])
                if (357+index) < len(sample):
                    sample[357+index] = 1
    except Exception as e:
        is_insert = False
    if is_insert is False:
        return "-1"
    else:
        return sample

if __name__=='__main__':
    print(len("a,".split(",")))
    # a = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # p = np.array(a)
    # print(p)
    # print("********")
    # print(p[2:])
    pass