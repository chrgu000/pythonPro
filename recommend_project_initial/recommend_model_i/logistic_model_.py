# -*- coding: utf-8 -*

import sys
sys.path.append("../")
from trainset.get_trainset import get_pos_trainset,get_pos_trainset_r,get_neg_trainset,get_neg_trainset_r
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from fea_engineering.get_features import feature_trans
from fea_engineering.get_features import samples_label
from sklearn.metrics import roc_curve,auc
from sklearn.metrics import log_loss
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from random_select import features_engineering_test,get_test_cid,get_samples
from sklearn.model_selection import KFold

def logistic_recommend(code):

    '''
    推荐算法：GBDT+LR
        get_pos_trainset():获取客户正样本
        get_neg_trainset():获取客户负样本（方式一）
        get_neg_trainset_r():获取客户负样本（方式二）
        features_engineering():通过clue_id 对应特征表，并做特征处理工作
        samples_label():贴正负样本的标签
    '''
    # pos_sam_id = get_pos_trainset(code)
    pos_sam_id = get_pos_trainset_r(code)

    # neg_sam_id_1 =get_neg_trainset(code)  #不感兴趣
    neg_sam_id_2=get_neg_trainset_r(len(pos_sam_id)) #随机抽取

    # neg_sam_id_3=neg_sam_id_1 #混合
    # for i in range(0,len(neg_sam_id_2)):
    #     neg_sam_id_3.append(neg_sam_id_2[i])

    train_sets=feature_trans(pos_sam_id,neg_sam_id_2)
    labels=samples_label(pos_sam_id,neg_sam_id_2)

    # 切分为测试集和训练集，比例0.5
    X_train, X_test, y_train, y_test = train_test_split(train_sets, labels, test_size=0.5)
    # 将训练集切分为两部分，一部分用于训练GBDT模型，另一部分输入到训练好的GBDT模型生成GBDT特征，然后作为LR的特征。这样分成两部分是为了防止过拟合。
    X_train_g, X_train_lr, y_train_g, y_train_lr = train_test_split(X_train, y_train, test_size=0.5)
    # 调用GBDT分类模型。
    gbdt = GradientBoostingClassifier(n_estimators=5)
    # 调用one-hot编码。
    gbdt_enc = OneHotEncoder()
    # 调用LR分类模型。
    lr = linear_model.LogisticRegression()
    # 用于做对比的LR模型
    lr_contrast=linear_model.LogisticRegression()

    # 使用X_train训练GBDT模型，后面用此模型构造特征
    gbdt.fit(X_train_g, y_train_g)
    joblib.dump(gbdt,code+"_gbdt.m")
    # fit one-hot编码器
    gbdt_enc.fit(gbdt.apply(X_train_g)[:, :, 0])
    joblib.dump(gbdt_enc,code+"_onehot.m")
    # 使用训练好的GBDT模型构建特征，然后将特征经过one-hot编码作为新的特征输入到LR模型训练

    lr.fit(gbdt_enc.transform(gbdt.apply(X_train_lr)[:, :, 0]), y_train_lr)
    lr_contrast.fit(X_train_lr,y_train_lr)
    # save LR_Model
    joblib.dump(lr, code + "_lr.m")
    joblib.dump(lr_contrast,code+"_lr_contrast.m")

    # 用训练好的LR模型X_test做预测
    y_pred_grd_lm = lr.predict_proba(gbdt_enc.transform(gbdt.apply(X_test)[:, :, 0]))[:, 1]
    y_pre=lr.predict(gbdt_enc.transform(gbdt.apply(X_test)[:, :, 0]))
    y_pred_grd_lm_contrast = lr_contrast.predict_proba(X_test)[:, 1]
    y_pre_c=lr_contrast.predict(X_test)

    # 根据预测结果输出
    fpr_grd_lm, tpr_grd_lm, _ = roc_curve(y_test,y_pred_grd_lm)
    cmatrix=confusion_matrix(y_test,y_pre)
    fpr_grd_lm_c, tpr_grd_lm_c, _c = roc_curve(y_test,y_pred_grd_lm_contrast)
    cmatrix_c =confusion_matrix(y_test,y_pre_c)
    target_names=['class0','class1']
    c_report=classification_report(y_test,y_pre,target_names=target_names)
    c_report_c=classification_report(y_test,y_pre_c,target_names=target_names)

    score=auc(fpr_grd_lm,tpr_grd_lm)
    score_c=auc(fpr_grd_lm_c,tpr_grd_lm_c)
    logloss_score=log_loss(y_test,y_pred_grd_lm)
    logloss_score_c=log_loss(y_test,y_pred_grd_lm_contrast)
    print("gbdt+lr confusion matrix,auc,logloss,classification:")
    print(cmatrix)
    print(score)
    print(logloss_score)
    print(c_report)
    print("lr confusion matrix,auc,logloss,classification:")
    print(cmatrix_c)
    print(score_c)
    print(logloss_score_c)
    print(c_report_c)

def test_model(code):
    llr = joblib.load(code + "_lr.m")
    r_test_sets = features_engineering_test(1000, 100)
    cid_list=get_test_cid(1000, 100)
    pos_cid_list=[]
    neg_cid_list=[]
    gbdt=joblib.load(code + "_gbdt.m")
    gbdt_enc=joblib.load(code + "_onehot.m")
    y_pred_grd_lm_r = llr.predict_proba(gbdt_enc.transform(gbdt.apply(r_test_sets)[:, :, 0]))[:, 1]

    for i in range(0,len(y_pred_grd_lm_r)):
        if y_pred_grd_lm_r[i]>0.5:pos_cid_list.append(cid_list[i])
        else:neg_cid_list.append(cid_list[i])

    print(pos_cid_list)
    print("-------------------------")
    print(neg_cid_list)
    # pos_row = get_samples(pos_cid_list)
    # # 将正样本负样本存到两个文件，用于查看推荐结果信息
    # file_pos = open("pos_samples.csv", 'a')
    # for i in range(0, len(pos_row)):
    #     file_pos.write(str(pos_row[i]))
    #     file_pos.write('\n')
    # file_pos.close()
    # neg_row = get_samples(neg_cid_list)
    # file_neg = open("neg_samples.csv", 'a')
    # for i in range(0, len(neg_row)):
    #     file_neg.write(str(neg_row[i]))
    #     file_neg.write('\n')
    # file_neg.close()

if __name__=='__main__':
    code="yunkecn"
    logistic_recommend(code)
    print("success!")

    # test_model(code)

    # gbt=joblib.load("yunkecn_gbdt.")
    # onehot=joblib.load("yunkecn_onehot.m")
    # lr_1=joblib.load("yunkecn.lr.m")
    # lr_2=joblib.load("yunkecn_lr_contrast.m")
    pass