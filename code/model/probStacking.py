#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-10-10 下午8:06
# @Author  : sunday
# @Site    : 
# @File    : probStacking.py
# @Software: PyCharm


from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier #GBM algorithm
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import lightgbm


from sklearn import preprocessing
# from create_submission import create_submission
prob_path = unicode(r'../output/submission_case.csv', 'utf-8')

all_data_file = unicode(r'../input/特征处理后的train.csv', 'utf-8')
train_X = pd.read_csv(all_data_file)
#删除异常数据
train_X.drop(10680,axis=0,inplace=True)
train_X.drop(9483,axis=0,inplace=True)
train_X.drop(8735,axis=0,inplace=True)

test_data_file = unicode(r'../input/特征处理后的test.csv', 'utf-8')
test_data = pd.read_csv(test_data_file)
testVar20 = pd.read_csv(r'../input/test_var20MapRes.csv')
trainVar20 = pd.read_csv(r'../input/train_var20MapRes.csv')
train_data = pd.merge(train_X,trainVar20,on='id')
test_data = pd.merge(test_data,testVar20,on='id')


testVar19Path = unicode(r'../input/数据集/testVar19.csv', 'utf-8')
testVar19 = pd.read_csv(testVar19Path)
trainVar19Path = unicode(r'../input/数据集/trainVar19.csv', 'utf-8')
trainVar19 = pd.read_csv(trainVar19Path)
#
testVar126FeaturePath = unicode(r'../input/数据集/testVar126Feature.csv', 'utf-8')
testVar126Feature = pd.read_csv(testVar126FeaturePath)
trainVar126FeaturePath = unicode(r'../input/数据集/trainVar126Feature.csv', 'utf-8')
trainVar126Feature = pd.read_csv(trainVar126FeaturePath)

numericTestDFPath = unicode(r'../input/last/numericTestDF.csv', 'utf-8')
numericTestDF = pd.read_csv(numericTestDFPath)
numericTrainDFPath = unicode(r'../input/last/numericTrainDF.csv', 'utf-8')
numericTrainDF = pd.read_csv(numericTrainDFPath)

train_data = pd.merge(train_data,trainVar19,on='id')
train_data = pd.merge(train_data,trainVar126Feature,on='id')
train_data = pd.merge(train_data,numericTrainDF,on='id')

test_data = pd.merge(test_data,testVar19,on='id')
test_data = pd.merge(test_data,testVar126Feature,on='id')
test_data = pd.merge(test_data,numericTestDF,on='id')



train_data.sample(frac=1)
target = 'target'
IDcol = 'id'

#
feature_imp_path = unicode(r'../output/xgb_feature_score.csv', 'utf-8')
features = []
with open(feature_imp_path, 'r') as fea_imp:
    for i in fea_imp:
        lists = i.split(',')
        features.append(lists[0])
predictors =features





'''模型融合中使用到的各个单模型'''
from sklearn.ensemble import AdaBoostClassifier
clfs = [


        XGBClassifier(
                    learning_rate=0.05,
                    n_estimators=340,
                    max_depth=4,
                    min_child_weight=6,
                    gamma=0.1,
                    subsample=0.7,
                    colsample_bytree=0.9,
                    objective='binary:logistic',
                    nthread=4,
                    scale_pos_weight=1,
                    seed=27,
                ),

        XGBClassifier(
            learning_rate=0.05,
            n_estimators=320,
            max_depth=4,
            min_child_weight=6,
            gamma=0.1,
            subsample=0.7,
            colsample_bytree=0.9,
            objective='binary:logistic',
            nthread=4,
            scale_pos_weight=1,
            seed=15,
            reg_lambda=1
        ),
        LogisticRegression()


        ]






X, y = train_data[0:24309][predictors].values,train_data['target'].values
X_predict = test_data[:][predictors].values




dataset_blend_train = np.zeros((X.shape[0], len(clfs)))
dataset_blend_test = np.zeros((X_predict.shape[0], len(clfs)))

'''5折stacking'''
n_folds = 5
skf = list(StratifiedKFold(y, n_folds,shuffle=True))

  


for j, clf in enumerate(clfs):
    '''依次训练各个单模型'''
    print(j, clf)
    # dataset_blend_test_j = np.zeros((X_predict.shape[0], len(skf)))
    clf.fit(X, y)
    dataset_blend_test[:, j] = clf.predict_proba(X_predict)[:, 1]

y_submission = dataset_blend_train[:, 0]*0.33+dataset_blend_train[:, 1]*0.65+dataset_blend_train[:, 2]*0.02


# clf = LogisticRegression()
# clf2 = XGBClassifier(learning_rate=0.05, subsample=0.5, max_depth=4, n_estimators=90)
# clf = GradientBoostingClassifier(learning_rate=0.02, subsample=0.5, max_depth=5, n_estimators=40)

# clf = XGBClassifier(learning_rate=0.05,objective='binary:logistic',min_child_weight=8)
# clf.fit(dataset_blend_train, y)
# y_submission = clf.predict_proba(dataset_blend_test)[:, 1]
print("Linear stretch of predictions to [0,1]")
# y_submission = (y_submission - y_submission.min()) / (y_submission.max() - y_submission.min())
# print("blend result")
# print("val auc Score: %f" % (roc_auc_score(y_predict, y_submission)))


# y_sub = dataset_blend_test[:,0]
# print("val auc Score: %f" % (roc_auc_score(y_predict, y_sub)))

#create submission file
submission = pd.DataFrame(data={"id": test_data.id, "predict": y_submission})
submission.to_csv(prob_path, index=False)