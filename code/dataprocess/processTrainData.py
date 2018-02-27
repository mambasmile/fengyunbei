#coding=utf-8

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

"""删除异常数据点"""
traindf.drop(8735,inplace=True)
traindf.drop(9483,inplace=True)
traindf.drop(10680,inplace=True)

testdf = pd.read_csv('../trainFile/test.csv',encoding='gbk')
df = pd.concat([traindf,testdf],axis=0)

deleteFeatureLs = ['var20','var21','var22','var23','var24','var25','var45','var58',
               'var124','var125','var126',
                   'var134','var135']

"""将字段值的种类数小于等于10的视作种类特征，需要ong-hot编码"""
# varietyFeature,numericFeature = readExcel('../trainFile/zeroInfo.xls')
varietyFeature,numericFeature = [],df.columns.tolist()
numericFeature.remove('target')
numericFeature.remove('id')

"""删除数据集中的文本特征"""
for fea in deleteFeatureLs:
    df.pop(fea)
    if fea in varietyFeature:
        varietyFeature.remove(fea)
    if fea in numericFeature:
        numericFeature.remove(fea)

# for fea in ['var77', 'var78', 'var79', 'var80', 'var73', 'var74', 'var75', 'var76', 'var32', 'var42', 'var52', 'var63', 'var34', 'var44', 'var124', 'var119', 'var121', 'var122', 'var123', 'var118', 'var120', 'var115', 'var116', 'var117']:
#     if fea in deleteFeatureLs:
#         continue
#     df.pop(fea)
#     if fea in varietyFeature:
#         varietyFeature.remove(fea)
#     if fea in numericFeature:
#         numericFeature.remove(fea)

# for index in xrange(489,533):
#     fea = 'var'+str(index)
#     df.pop(fea)
#     if fea in varietyFeature:
#         varietyFeature.remove(fea)
#     if fea in numericFeature:
#         numericFeature.remove(fea)

print 'var489' in varietyFeature

"""将var19 类别数据数字化"""
class_mapping = {label:idx for idx,label in enumerate(np.unique(df['var19']))}
var19dict = {u'私企公司职工':1,u'公司受雇员工':1,u'国企事业单位职工':2,
             u'自雇创业人员':3,u'农林牧副渔人员':3,u'自主创业人员':3,
             u'公务员':2,u'自由职业者':4,u'司机':1,u'厨师':1,u'军人':2,
             u'品质主管':1,u'公司受雇店长':1,u'单位职工':1,u'部长':2,u'快递':1,u'失业人员':5,
             u'拓展部经理':1,u'快递员':1,u'销售部长':1,
u'员工':1,
u'民营事业单位职工':1,
u'经理':1,
u'销售管理':1,
u'普通员工':1,
u'职工':1,
u'家庭主妇':5,
u'后厨':1,
u'技术员':1,
u'受雇员工':1,
u'前台':1,
u'负责人':1,
u'技工':1,
u'公司员工':1,
u'销售经理':1,
u'高管':1,
u'创业人员':2,
u'一般员工':1,
u'厨房':1,
u'生产主管':1,
u'设计师':1,
u'副店长':1,}

df['newVar19'] = df.var19
df.var19 = df.var19.map(class_mapping)
df['newVar19'] = df['newVar19'].map(var19dict)
df.var19 = df.var19.astype(str)
df['newVar19']  = df['newVar19'].astype(str)
if 'var19' in numericFeature:
    numericFeature.remove('var19')
varietyFeature.append('var19')
varietyFeature.append('newVar19')

"""种类特征进行one-hot编码"""
for val in ['var3','var11','var16','var17','var18']:
    if val not in varietyFeature:
        varietyFeature.append(val)
    if val in numericFeature:
        numericFeature.remove(val)

featureDict = df.isnull().sum().to_dict()

print numericFeature.__len__()
print varietyFeature.__len__()

"""缺失值填充"""
for key in featureDict:
    if featureDict[key] > 0:
        fillFeature(df, key, df[key].quantile(0.5))
        # if key in varietyFeature:
        #     tmpLs = df[key].unique().tolist()
        #     try:
        #         resLs = np.isnan(tmpLs)
        #     except TypeError,e:
        #         print e,key
        #     value = max([tmpLs[i] for i in xrange(len(resLs)) if resLs[i] == False])+1
        #     fillFeature(df,key,value)
        #     continue
        # if key in numericFeature:
        #     try:
        #         fillFeature(df,key, df[key].quantile(0.5))
        #     except TypeError,e:
        #         print e,key
print df.shape


"""对种类特征进行one-hot编码"""
for fea in varietyFeature:
    df[fea] = df[fea].astype(str)
#     numericFeature.remove(fea)
df = pd.get_dummies(df)

for fea in numericFeature:
    df[fea] = (df[fea]-np.min(df[fea]))/(float)(np.max(df[fea])-np.min(df[fea]))

for fea in df.columns.tolist():
    if df[fea].isnull().any():
        print fea
print df.isnull().any().any()

# df.iloc[:24306,:].to_csv('../trainFile/非标准化的特征处理后的train.csv',encoding='gbk',index=False)
# df.iloc[24306:,:].to_csv('../trainFile/非标准化的特征处理后的test.csv',encoding='gbk',index=False)

"""不删除特征"""
# df.iloc[:24306,:].to_csv('../trainFile/特征处理后的train.csv',encoding='gbk',index=False)
# df.iloc[24306:,:].to_csv('../trainFile/特征处理后的test.csv',encoding='gbk',index=False)

"""删除var489之后的特征"""
# df.iloc[:24306,:].to_csv('../trainFile/特征处理后的train1.csv',encoding='gbk',index=False)
# df.iloc[24306:,:].to_csv('../trainFile/特征处理后的test1.csv',encoding='gbk',index=False)

"""删除更多的特征"""
# df.iloc[:24306,:].to_csv('../trainFile/特征处理后的train2.csv',encoding='gbk',index=False)
# df.iloc[24306:,:].to_csv('../trainFile/特征处理后的test2.csv',encoding='gbk',index=False)

# df.iloc[:24306,:].to_csv('../trainFile/非标准化的特征处理后的train2.csv',encoding='gbk',index=False)
# df.iloc[24306:,:].to_csv('../trainFile/非标准化的特征处理后的test2.csv',encoding='gbk',index=False)

"""自己不增加种类特征"""
df.iloc[:24306,:].to_csv('../trainFile/原始数据特征处理后的train1.csv',encoding='gbk',index=False)
df.iloc[24306:,:].to_csv('../trainFile/原始数据特征处理后的test1.csv',encoding='gbk',index=False)

"""删除var489之后的特征"""
# df.iloc[:24306, :].to_csv('../trainFile/原始数据特征处理后的train2.csv', encoding='gbk', index=False)
# df.iloc[24306:, :].to_csv('../trainFile/原始数据特征处理后的test2.csv', encoding='gbk', index=False)

"""删除更多的特征"""
# df.iloc[:24306, :].to_csv('../trainFile/原始数据特征处理后的train3.csv', encoding='gbk', index=False)
# df.iloc[24306:, :].to_csv('../trainFile/原始数据特征处理后的test3.csv', encoding='gbk', index=False)
