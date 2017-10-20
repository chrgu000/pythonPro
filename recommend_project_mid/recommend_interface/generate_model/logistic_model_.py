# -*- coding: utf-8 -*

import sys
sys.path.append("../..")
sys.path.append("../")
from generate_model.get_trainset import get_pos_trainset_r, get_neg_trainset_r
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from generate_model.get_features import feature_trans
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder

def logistic_recommend(code):
    is_model_generate = True
    pos_sam_id = get_pos_trainset_r(code)
    neg_sam_id_2 = get_neg_trainset_r(len(pos_sam_id),pos_sam_id) #随机抽取
    results = feature_trans(pos_sam_id, neg_sam_id_2)
    train_sets = results[0]
    labels = results[1]

    if len(train_sets) >= 2:
        try:
            x_train_g, x_train_lr, y_train_g, y_train_lr = train_test_split(train_sets, labels, test_size=0.5)
            gbdt = GradientBoostingClassifier(n_estimators=5)
            onehot = OneHotEncoder()
            lr = linear_model.LogisticRegression()
            gbdt.fit(x_train_g, y_train_g)
            joblib.dump(gbdt, "../model/gbdt/"+code+"_gbdt.m")
            onehot.fit(gbdt.apply(x_train_g)[:, :, 0])
            joblib.dump(onehot, "../model/onehot/"+code+"_onehot.m")
            lr.fit(onehot.transform(gbdt.apply(x_train_lr)[:, :, 0]), y_train_lr)
            # save LR_Model
            joblib.dump(lr, "../model/lr/"+code + "_lr.m")
        except Exception as e:
            print(e)
            is_model_generate = False
    return is_model_generate

if __name__=='__main__':
    file = open("../../model/cur_company.txt", encoding='utf8', errors='ignore')
    company_list = file.readlines()
    company_dict = {}
    for c in company_list:
        c = c.replace("\n","")
        if c not in company_dict.keys():
            company_dict[c] = 1
        else:
            company_dict[c] += 1
    for k, v in company_dict.items():
        print(k)
        logistic_recommend(k)

    pass