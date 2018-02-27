#coding=utf-8

import pandas as pd
import json
from checkNumericFeature import readNumericFeature
from writeExcel import readExcel

"""
对var19字段，根据不同职业的收入水平，“无收入”，“低收入”，“一般收入”，“高收入”划分为4类，并进行one-hot编码

对特征进行组合，形成新的特征

"""

def findFea(featureLs,feature_name):
    resLs = []
    for fea in featureLs:
        data = fea.strip().split('_')
        if data[0] == feature_name:
            resLs.append(fea)
    return resLs

def buildnewFeature(df,formerFeaLs,laterFeaLs):
    resLs = []
    for fea1 in formerFeaLs:
        for fea2 in laterFeaLs:
            tmpSeries = (df[fea1]*df[fea2]).unique().tolist()
            if tmpSeries.__len__() == 2 and tmpSeries[0] == 0:
                resLs.append([fea1, fea2])
            # else:
            #     resLs.append([fea1,fea2])
    return resLs

def anlysisVar19(df,filepath):
    resLs = []
    idLs = df.id.tolist()
    var19Ls = df.var19.tolist()
    print var19Ls.__len__()
    print idLs.__len__()
    for i in xrange(var19Ls.__len__()):
        val = var19Ls[i]
        if val in [u'私企公司职工',u'公司受雇员工',u'国企事业单位职工',u'公务员',u'自由职业者',u'司机',u'厨师',u'军人',u'单位职工',
                              u'快递员',u'快递',u'员工',u'民营事业单位职工',u'普通员工',u'职工',u'前台',u'后厨',u'技术员',u'受雇员工',u'公司员工',
                              u'一般员工',u'厨房']:
            resLs.append(1)
        elif val in [u'品质主管',u'公司受雇店长',u'部长',u'经理',u'销售管理',u'负责人',u'技工',u'销售经理',u'高管',u'生产主管',u'设计师',u'副店长',
                                u'拓展部经理', u'销售部长',]:
            resLs.append(2)
        elif val in [u'自雇创业人员',u'农林牧副渔人员',u'自主创业人员',u'创业人员']:
            resLs.append(3)
        elif val in [u'失业人员',u'家庭主妇']:
            resLs.append(4)
        else:
            print val
    print resLs.__len__()
    with open(filepath,'w') as e:
        e.write("id,workKind"+'\n')
        for i in xrange(len(idLs)):
            e.write(",".join([str(idLs[i]),str(resLs[i])])+'\n')




# trainDF = pd.read_csv('../trainFile/特征处理后的train3.csv')
# testDF = pd.read_csv('../trainFile/特征处理后的test3.csv')
# df = pd.concat([trainDF,testDF],axis=0)
#
# resDF = df[['id']]
#
# selectFeatures = set()
# i=0
# with open('../trainFile/分类特征权重1.csv','r') as e:
#     for line in e:
#         i+=1
#         data = line.strip().split(',')
#         selectFeatures.add(data[0].split('_')[0])
#         if i>=100:
#             break
#
# resSet = []
# with open('../trainFile/特征组合.txt','r') as e:
#     for line in e:
#         resLs = json.loads(line)
# print resLs.__len__()
# count = 0
# for tmpls in resLs:
#     data = tmpls[0].split('_')
#     data1 = tmpls[1].split('_')
#     if data[0] in selectFeatures and data1[0] in selectFeatures:
#         resSet.append(tmpls)
#
# for tmpls in resSet:
#     val = '*'.join(tmpls)
#     resDF[val] = df[tmpls[0]] * df[tmpls[1]]
#
# resDF.iloc[:24309,:].to_csv('../trainFile/moreVarTrain.csv',encoding='gbk',index=False)
# resDF.iloc[24309:,:].to_csv('../trainFile/moreVarTest.csv',encoding='gbk',index=False)

def splitNumericFeature(df,featureName):
    for feature in featureName:
        classMapping = {}
        maxValue = max(df[feature])
        minValue = min(df[feature])
        value = (maxValue-minValue)/5.0
        valueList = df[feature].unique().tolist()
        for i in xrange(10):
            for val in valueList:
                if val >=(minValue+i*value) and val<(minValue+(i+1)*value):
                    classMapping[val] = i
        classMapping[maxValue] = 9
        df[feature] = df[feature].map(classMapping)
        df[feature] = df[feature].astype(str)
        df = pd.get_dummies(df,[feature])
    return df

def splitNumericFeatureToCsv(trainDF,testDF,featureName,trainFile,testFile):
    df = pd.concat([trainDF,testDF],axis=0)

    subTrainDF = trainDF[['id']]
    subTestDF = testDF[['id']]

    featureName.append('id')
    tmpDF = df[featureName].copy()
    for feature in featureName:
        if feature == 'id':
            continue
        classMapping = {}
        maxValue = max(tmpDF[feature])
        minValue = min(tmpDF[feature])
        value = (maxValue-minValue)/5.0
        valueList = tmpDF[feature].unique().tolist()
        for i in xrange(10):
            for val in valueList:
                if val >=(minValue+i*value) and val<(minValue+(i+1)*value):
                    classMapping[val] = i
        classMapping[maxValue] = 9
        tmpDF[feature] = tmpDF[feature].map(classMapping)
        tmpDF[feature] = tmpDF[feature].astype(str)
        tmpDF = pd.get_dummies(tmpDF,[feature])
    trainDF = tmpDF.iloc[:24306,:]
    testDF = tmpDF.iloc[24306:,:]

    trainDF = pd.merge(trainDF,subTrainDF,on='id')
    testDF = pd.merge(testDF,subTestDF,on='id')

    trainDF.to_csv(trainFile,index=False)
    testDF.to_csv(testFile,index=False)

if __name__ == '__main__':

    """对var19特征属性进行等级划分"""
    # trainDF = pd.read_csv('../trainFile/train.csv',encoding='gbk')
    # anlysisVar19(trainDF, '../trainFile/trainVar19_1.csv')
    # testDF = pd.read_csv('../trainFile/test.csv',encoding='gbk')
    # anlysisVar19(testDF, '../trainFile/testVar19_1.csv')

    # var19trainDF = pd.read_csv('../trainFile/trainVar19_1.csv')
    # print var19trainDF.shape
    # var19trainDF.drop(8735, inplace=True)
    # var19trainDF.drop(9483, inplace=True)
    # var19trainDF.drop(10680, inplace=True)
    # var19testDF = pd.read_csv('../trainFile/testVar19_1.csv')
    # print var19testDF.shape
    # var19DF = pd.concat([var19trainDF,var19testDF],axis=0)
    # var19DF.workKind = var19DF.workKind.astype(str)
    # var19DF = pd.get_dummies(var19DF,['workKind'])
    # print var19DF.shape
    # var19DF.iloc[:24306,:].to_csv('../trainFile/trainVar19.csv',index=False)
    # var19DF.iloc[24306:,:].to_csv('../trainFile/testVar19.csv',index=False)
    # print 'hello'

    """对数值特征进行切分"""
    # _,numericFeature = readExcel('../trainFile/zeroInfo.xls')
    # numericFeature.remove('var19')
    # for val in ['var3', 'var11', 'var16', 'var17', 'var18']:
    #     if val in numericFeature:
    #         numericFeature.remove(val)
    #
    # trainDF = pd.read_csv('../trainFile/非标准化的特征处理后的train.csv')
    # print trainDF.shape
    # testDF = pd.read_csv('../trainFile/非标准化的特征处理后的test.csv')
    # print testDF.shape
    # allDF = pd.concat([trainDF,testDF],axis=0)
    # resDF = splitNumericFeature(allDF,numericFeature)
    #
    # resTestDF = resDF.iloc[24306:,:]
    # resTestDF.pop('target')
    # resDF.iloc[:24306,:].to_csv('../trainFile/特征处理后的train4.csv',index=False)
    # resTestDF.to_csv('../trainFile/特征处理后的test4.csv',index=False)
    #
    # df = pd.read_csv('../trainFile/特征处理后的train4.csv')
    # print df.shape

    """将数值特征离散化后直接写入文件"""
    trainDF = pd.read_csv('../trainFile/非标准化的特征处理后的train.csv')
    testDF = pd.read_csv('../trainFile/非标准化的特征处理后的test.csv')
    _, numericFeature = readExcel('../trainFile/zeroInfo.xls')

    # for fea in ['var77', 'var78', 'var79', 'var80', 'var73', 'var74', 'var75', 'var76', 'var32', 'var42', 'var52',
    #             'var63', 'var34', 'var44', 'var124', 'var119', 'var121', 'var122', 'var123', 'var118', 'var120',
    #             'var115', 'var116', 'var117']:
    #     if fea in numericFeature:
    #         numericFeature.remove(fea)

    print '----'
    numericFeature.remove('var19')
    for val in ['var3', 'var11', 'var16', 'var17', 'var18']:
        if val in numericFeature:
            numericFeature.remove(val)
    splitNumericFeatureToCsv(trainDF,testDF,numericFeature,'../validateData/numericTrainDF1.csv','../validateData/numericTestDF1.csv')
