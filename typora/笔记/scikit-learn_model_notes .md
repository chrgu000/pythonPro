# scikit-learn model params 

## LogisticRegression

 LR模型:scikit-learn中，与逻辑回归有关的:LogisticRegression,LogisticRegressionCV,logistic_regression_path
    LogisticRegression:
     penalty:默认l2，可选l1,l2
         l2 ->{newton-cg,lbfgs,sag};l1->{liblinear,saga}
    solver: {newton-cg,lbfgs,liblinear,sag,saga},默认：liblinear
        samll datasets ->{liblinear};large datasets->{sag,saga}
        multiclass problems->{newton-cg,sag,saga,lbfgs};OvR->{newton-cg,lbfgs,liblinear,sag,saga}
    a) liblinear：使用了开源的liblinear库实现，内部使用了坐标轴下降法来迭代优化损失函数。
    b) lbfgs：拟牛顿法的一种，利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数。
    c) newton-cg：也是牛顿法家族的一种，利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数。
    d) sag：即随机平均梯度下降，是梯度下降法的变种，和普通梯度下降法的区别是每次迭代仅仅用一部分的样本来计算梯度，适合于样本数据多的时候，SAG是一种线性收敛算法，这个速度远比SGD快
    class_weight:分类模型中各种类型的权重，可以不输入
    sample_weight:调用fit函数时，通过sample_weight调节每个样本权重.
    scikit-learn做逻辑回归时，如果上面两种方法都用到了，那么样本的真正权重是class_weight*sample_weight   
    C: 默认:1.0 
    other:dual:tol:fit_intercept:intercept_scaling:random_state:max_iter:multi_class:verbose:warm_start:n_jobs:

## GradientBoostingClassifier(gbdt)

gdbt预选择特征
    boosting框架参数：
        n_estimators:弱学习器最大迭代次数
        learing_rate:步长，每个弱学习器权重缩减系数
        subsample:子采集（不放回抽样）
        init:
        loss:损失函数计算方式（对数似然损失函数deviance，指数损失函数exponential）
        alpha:这个参数只有GradientBoostingRegressor有，使用Huber损失"huber"和分位数损失“quantile”时，需要指定分位数的值。默认是0.9，如果噪音点较多，可以适当降低这个分位数的值
    gbdt弱学习器参数：
        max_feature:划分时考虑的最大特征数
        max_depth:决策树最大深度
        min_samples_split:内部节点再划分所需最小样本数
        min_samples_leaf:叶子节点最少样本数
        min_weight_fraction_leaf:叶子节点最小的样本权重和
        max_leaf_nodel:最大叶子节点数
        min_impurity_split:节点划分最小不纯度（一般不推荐改动默认值1e-7）
    other:
        warm_start:presort:criterion :init:verbose:warm_start:random_state:


## sklearn.metrics

    accuracy_score:可用于两分类和多分类
    auc:
    average_precision_score:值的平均准确率，precision-recall曲线下的面积
    classification_report
## sklearn.model_selection.KFold

为充分使用数据集对算法效果的测试，KFold将数据集随机分成K个数据集，每次取其中一个数据集作为测试集，余下数据集作为训练集用来训练模型

参数：n_splits: int类型，默认值=3

