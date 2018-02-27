#coding=utf-8

"""
检查数字特征，检查种类特征

"""

import pandas as pd

def readNumericFeature():
    traindf = pd.read_csv('../trainFile/train.csv',encoding='gbk')
    testdf = pd.read_csv('../trainFile/test.csv',encoding='gbk')
    df = pd.concat([traindf,testdf],axis=0)

    # for index in xrange(489,533):
    #     df.pop('var'+str(index))

    featureList = df.columns.tolist()
    featureList.remove('id')
    featureList.remove('target')

    deleteFeature = ['var19','var20','var21','var22','var23','var24','var25','var45','var58','var124','var125','var126',]
    varietyFeature = [fea for fea in featureList if df[fea].unique().tolist().__len__() >=2 and df[fea].unique().tolist().__len__() <=10]
    numericFeature = [fea for fea in featureList if fea not in varietyFeature and fea not in deleteFeature]
    # print featureList
    # print varietyFeature
    print varietyFeature
    return numericFeature

readNumericFeature()


