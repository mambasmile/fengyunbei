#coding=utf-8

import pandas as pd
import matplotlib.pyplot as plt

"""
var20表示省
var21表示城市
将字段var20，var21合并为一个字段“省市”处理；计算对应省市下target为1的比例，以75%为标准线将省市划分为两类，
一类表示target为1的比例较高的省市
一类表示target为1的比例较低的省市
"""

# test_df = pd.read_csv('../trainFile/testVar20_1.csv',encoding='gbk')
# train_df = pd.read_csv('../trainFile/trainVar20_1.csv',encoding='gbk')
# df = pd.concat([train_df,test_df])
#
# classMapping = {label:ix for ix,label in enumerate(df['var20'])}
# # print sorted(classMapping.values())
#
# df['var20'] = df['var20'].map(classMapping)
# df['var20'] = df['var20'].astype(str)
#
# #
# # # test_df['var20'] = test_df['var20'].map(classMapping)
# # # train_df['var20'] = train_df['var20'].map(classMapping)
# # #
# # # train_df.to_csv('../trainFile/trainVar20.csv',index=False)
# # # test_df.to_csv('../trainFile/testVar20.csv',index=False)
# df = pd.get_dummies(df)
# df.iloc[:24309,:].to_csv('../trainFile/trainVar20.csv',index=False,encoding='gbk')
# df.iloc[24309:,:].to_csv('../trainFile/testVar20.csv',index=False,encoding='gbk')
#
# # df = pd.read_csv('../trainFile/trainVar20.csv',encoding='gbk')
# # print df.columns

"""进一步处理区域"""
# train_df1 = pd.read_csv('../trainFile/trainVar20_1.csv',encoding='gbk')
# train_df2 = pd.read_csv('../trainFile/trainVar21_1.csv',encoding='gbk')
#
# test_df1 = pd.read_csv('../trainFile/testVar20_1.csv',encoding='gbk')
# test_df2 = pd.read_csv('../trainFile/testVar21_1.csv',encoding='gbk')
#
# sub_trainDF = pd.read_csv('../trainFile/特征处理后的train.csv')
# sub_testDF = pd.read_csv('../trainFile/特征处理后的test.csv')
# trainDF = pd.merge(train_df1, sub_trainDF[['id', 'target']], on='id')
# trainDF = pd.merge(trainDF, train_df2, on='id')
#
# testDF = pd.merge(test_df1,sub_testDF[['id','target']],on='id')
# testDF = pd.merge(testDF,test_df2,on='id')
# allDF = pd.concat([trainDF,testDF])
# print allDF.shape
# allDF['var20'] = allDF['var20'] + allDF['var21']
#
# classMapping = {label:ix for ix,label in enumerate(allDF['var20'])}
# allDF['var20'] = allDF['var20'].map(classMapping)
# allDF.pop('var21')
# print allDF.shape
# # plt.plot(tmpDF['var20'][tmpDF.target==1].value_counts() / tmpDF['var20'].value_counts())
# # plt.show()
#
# afterTrainDF = allDF.iloc[:24309,:]
# afterTestDF = allDF.iloc[24309:,:]
# print afterTestDF.shape
# afterTrainDF.to_csv('../trainFile/train_var20Map.csv',index=False,encoding='gbk')
# afterTestDF.to_csv('../trainFile/test_var20Map.csv',index=False,encoding='gbk')
# print (afterTrainDF['var20'][afterTrainDF.target == 1].value_counts() / afterTrainDF['var20'].value_counts()).to_csv('../trainFile/tmpRes.csv', encoding='gbk')

"""分析label比例在0.75左右的省市"""
# afterTrainDF = pd.read_csv('../trainFile/train_var20Map.csv')
# afterTrainDF.drop(8735,inplace=True)
# afterTrainDF.drop(9483,inplace=True)
# afterTrainDF.drop(10680,inplace=True)
#
#
# resDataFrame = pd.DataFrame(afterTrainDF['var20'][afterTrainDF.target == 1].value_counts() / afterTrainDF['var20'].value_counts())
# resDataFrame = resDataFrame.fillna(0.0)
# print resDataFrame.quantile(0.75)
# resDataFrame.to_csv('../trainFile/tmpRes1.csv', encoding='gbk')

afterTrainDF = pd.read_csv('../trainFile/train_var20Map.csv')
afterTrainDF.drop(8735,inplace=True)
afterTrainDF.drop(9483,inplace=True)
afterTrainDF.drop(10680,inplace=True)
afterTestDF = pd.read_csv('../trainFile/test_var20Map.csv')
afterTrainDF.pop('target')
afterTestDF.pop('target')
allDF = pd.concat([afterTrainDF,afterTestDF],axis=0)
cityNumberLs = allDF.var20.tolist()

df = pd.read_csv('../trainFile/tmpRes1.csv')
zeroLs = df.cityNumber[df.rate<df.rate.quantile(0.75)]
oneLs = df.cityNumber[df.rate>=df.rate.quantile(0.75)]
classMapping = {}
for key in cityNumberLs:
    if key in zeroLs:
        classMapping[key] = 0
    elif key in oneLs:
        classMapping[key] = 1
    else:
        classMapping[key] = 0
afterTrainDF.var20 = afterTrainDF.var20.map(classMapping)
afterTestDF.var20 = afterTestDF.var20.map(classMapping)

afterTrainDF.to_csv('../trainFile/train_var20MapRes.csv',index=False)
afterTestDF.to_csv('../trainFile/test_var20MapRes.csv',index=False)

# df = pd.read_csv('../trainFile/tmpRes.csv',encoding='gbk')
# df.fillna(0.0)
# resLs = df['cityNumber'][df['count']>0.253879].tolist()
#
# trainDF = pd.read_csv('../trainFile/train_var20Map.csv')
# testDF = pd.read_csv('../trainFile/test_var20Map.csv')
# cityNumberLs = trainDF['var20'].tolist()
# cityNumberLs.extend(testDF['var20'].tolist())
# print cityNumberLs
#
# classMapping = {}
# for val in cityNumberLs:
#     if val in resLs:
#         classMapping[val] = 1
#     else:
#         classMapping[val] = 0
# # classMapping = {label:val for val in cityNumberLs if val in resLs }
#
# trainDF['var20'] = trainDF['var20'].map(classMapping)
# testDF['var20'] = testDF['var20'].map(classMapping)
# trainDF.pop('target')
# testDF.pop('target')
#
# trainDF.to_csv('../trainFile/train_var20MapRes.csv',index=False)
# testDF.to_csv('../trainFile/test_var20MapRes.csv',index=False)

# print tmpDF['var20'][tmpDF.target==1].value_counts() / tmpDF['var20'].value_counts()
# print tmpDF['var20'][tmpDF.target==0].value_counts()
# print tmpDF['var20'][tmpDF.target==1].value_counts()
