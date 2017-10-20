# -*- coding: utf-8 -*
'''
sql()
feature_pro():给出特征表中的数据，对每一个特征再处理
'''
import numpy as np

def sql():
    return "select c_type,c_has_site,c_employees_min,c_employees_mean,c_employees_max,c_reg_capital,c_reg_date,c_reg_address,c_tyc_score,c_tyc_summary,p_major,c_reg_address_lon,c_reg_address_lat,c_tfidf_vec,Clue_Id from clue_feature "

def feature_pro(row):
    try:
        sample = np.zeros(70000)
        # sample = np.zeros(357)
        # 公司类型
        sample[0] = row[0]

        # 是否有网站
        sample[1] = row[1]

        # 公司员工最小值
        sample[2] = row[2]

        # 公司员工均值
        sample[3] = row[3]

        # 公司员工最大值
        sample[4] = row[4]

        # 注册资金
        sample[5] = row[5]

        # 注册日期
        sample[6] = row[6]

        # 地区做onehot处理
        if row[7] != 0 or len(str(row[7])) > 5:
            sample[7+int(str(row[7])[0:2])] = 1
            sample[7+100+int(str(row[7])[2:4])] = 1
            sample[7+100+100+int(str(row[7])[4:6])] = 1

        # 天眼评分
        sample[308] = row[8]

        # 天眼概览
        if len(str(row[9])) > 3:
            summery_dict = eval(row[9])
            for k,v in summery_dict.items():
                sample[309+int(k)] = v

        # 职位
        sample[354] = row[10]

        # 经纬度
        sample[355] = row[11]
        sample[356] = row[12]

        # 文本向量
        if row[13] != -1 and ";" not in row[13]:
            k_list = row[13].split(",")
            for i in range(0,len(k_list)-1):
                index = int(k_list[i])
                if (357+index) < len(sample):
                    sample[357+index] = 1
        return sample
    except Exception as e:
        return "-1"

if __name__=='__main__':
    print(len("a,".split(",")))
    # a = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # p = np.array(a)
    # print(p)
    # print("********")
    # print(p[2:])
    pass