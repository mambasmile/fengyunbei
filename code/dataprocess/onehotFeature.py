#coding=utf-8

"""
将字段取值种类小于等于10的字段视为种类型数据
从数据集中选出种类型数据进行onehot编码

"""

import numpy as np
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale,StandardScaler
from writeExcel import readExcel
from getMoreFeature import splitNumericFeatureToCsv

def fillFeature(df,featureName,number=None):
    if number == None:
        df[featureName] = df[featureName].fillna(
            df[featureName].mean())
    else:
        df[featureName] = df[featureName].fillna(
            number)

def classMap(df,featureName,number):
    class_mapping = {}
    keyLs = df[featureName].unique()
    for key in keyLs:
        if key == number:
            class_mapping[key] = 0
        else:
            class_mapping[key] = 1
    df[featureName] = df[featureName].map(class_mapping)

traindf = pd.read_csv('../trainFile/train.csv',encoding='gbk')
traindf.drop(8735,inplace=True)
traindf.drop(9483,inplace=True)
traindf.drop(10680,inplace=True)

testdf = pd.read_csv('../trainFile/test.csv',encoding='gbk')
df = pd.concat([traindf,testdf],axis=0)

deleteFeatureLs = ['var20','var21','var22','var23','var24','var25','var45','var58',
               'var124','var125','var126',
                   'var134','var135']

varietyFeature,numericFeature = readExcel('../trainFile/zeroInfo.xls')

print 'target' in numericFeature
print 'target' in varietyFeature

for fea in deleteFeatureLs:
    df.pop(fea)
    if fea in varietyFeature:
        varietyFeature.remove(fea)

"""将var19 类别数据数字化"""
df.pop('var19')

"""种类特征"""
for val in ['var3','var11','var16','var17','var18']:
    if val in varietyFeature:
        varietyFeature.remove(val)

featureDict = df.isnull().sum().to_dict()

print numericFeature.__len__()
print varietyFeature.__len__()

for key in featureDict:
    if featureDict[key] > 0:
        if key in varietyFeature:
            tmpLs = df[key].unique().tolist()
            try:
                resLs = np.isnan(tmpLs)
            except TypeError,e:
                print e,key
            value = max([tmpLs[i] for i in xrange(len(resLs)) if resLs[i] == False])+1
            fillFeature(df,key,value)
            continue
        if key in numericFeature:
            try:
                fillFeature(df,key, df[key].quantile(0.5))
            except TypeError,e:
                print e,key
print df.shape


"""one-hot编码"""
for fea in varietyFeature:
    df[fea] = df[fea].astype(str)

varietyFeature.append('id')
tmpDF = df[varietyFeature].copy()
varietyFeature.remove('id')
tmpDF = pd.get_dummies(tmpDF,varietyFeature)
tmpDF.iloc[:24306,:].to_csv('../trainFile/train进行onehot编码.csv',encoding='gbk',index=False)
tmpDF.iloc[24306:,:].to_csv('../trainFile/test进行onehot编码.csv',encoding='gbk',index=False)
