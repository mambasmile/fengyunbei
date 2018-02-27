#coding=utf-8

import pandas as pd
import codecs
import re

"""
以@为分割符号，切割var126字段；将字段中的“本地”替换为本记录的var20+var21的值
我们在本地建立了全国所有省市的字典，用于查找城市所在的省市
统计var126中出现的“不同城市的个数”，“不同省的个数”，以及“不同省所占的比例”

"""

def comProvinceNum(cityDict,cityName):
    ret = None
    for key in cityDict:
        for val in cityDict[key]:
            if cityName == val:
                ret = key
    return ret

def comCityNum(file,cityDict):
    i =0
    count=0
    resultDict = {}
    id = []
    cityNum = []
    provinceNum = []
    provinceRate = []

    with open(file,'r') as e:
        for line in e:
            if i==0:
                i+=1
                continue

            else:
                count+=1
                data = line.strip().split(',')
                id.append(data[0])

                if data[126] == "":
                    cityNum.append(0)
                    provinceNum.append(0)
                else:
                    tmpLs = data[126].split('@')
                    for val in tmpLs:
                        if comProvinceNum(cityDict,val) is None:
                            print val.decode('gbk').encode('gbk')
                    cityNum.append(tmpLs.__len__())
                    # print tmpLs

    resultDict['id'] = id
    resultDict['cityNum'] = cityNum
    return resultDict

def findCityName(cityDict,name):
    if u'市'.encode('utf-8') in name:
        name = name.replace(u'市'.encode('utf-8'),'')
    for key in cityDict:
        if name in cityDict[key]:
            return key
    return None

def replaceLocal(filepath,outpath,localCityDict):
    pattern = re.compile('\[\d+\]')
    with codecs.open(outpath,'w','gbk') as e1:
        with codecs.open(filepath,'r','gbk') as e:
            i = 0
            for line in e:
                line = pattern.sub('',line)
                line = line.replace('[','')
                line = line.replace(']','')
                tmpStr = u'本地'
                if tmpStr in line:
                    line = line.replace(tmpStr,localCityDict[i])
                i+=1
                e1.write(line)

def addProvince(filepath,outpath):
    with codecs.open(outpath,'w') as e:
        with codecs.open(filepath,'r') as e1:
            for line in e1:
                resultLs = []
                tmpStr = line.strip().replace('： ', ' ').split(' ')
                resultLs.append(tmpStr[0])
                for val in tmpStr[1:-1]:
                    resultLs.append(val)
                    resultLs.append(tmpStr[0]+val)
                resultLs.append(tmpStr[-1])
                e.write(' '.join(resultLs)+'\n')

def replaceSymbol(symbol,filepath,outpath):
    with codecs.open(outpath,'w') as e:
        with codecs.open(filepath,'r') as e1:
            for line in e1:
                e.write(line.replace(symbol,''))

def replaceCityByLine(numberLs,filepath,filepath1,outpath):
    resLs1 = []
    resLs2 = []
    with open(filepath,'r') as e:
        for line in e:
            resLs1.append(line.strip())
    with open(filepath1,'r') as e:
            for line in e:
                resLs2.append(line.strip().split(',')[-1])
    for i in numberLs:
        resLs1[i] = resLs2[i]
    with open(outpath,'w') as e:
        for val in resLs1:
            e.write(val+'\n')

def checkFile(numberLs,filepath,filepath1,outpath):
    res = []

    resLs1 = []
    resLs2 = []
    with open(filepath, 'r') as e:
        for line in e:
            resLs1.append(line.strip().split(',')[-1])
    with open(filepath1, 'r') as e:
        for line in e:
            resLs2.append(line.strip().split(',')[-1])
    for i in numberLs:
        if resLs1[i] != resLs2[i]:
            print i,resLs1[i].decode('gbk').encode('utf-8')
            resLs1[i] = resLs2[i]
            res.append(i)
    with open(outpath, 'w') as e:
        for val in resLs1:
            e.write(val + '\n')
    print res

if __name__ == '__main__':
    """修改省以及市民"""
    # addProvince('../trainFile/model.txt','../trainFile/cityInformation.csv')

    # trainDF = pd.read_csv('../trainFile/train.csv',encoding='gbk')
    # testDF = pd.read_csv('../trainFile/test.csv',encoding='gbk')
    # allDF = pd.concat([trainDF,testDF],axis=0)
    # allDF.iloc[:24309,:].var126.to_csv('../trainFile/trainVar126.csv',encoding='gbk')
    # allDF.iloc[24309:,:].var126.to_csv('../trainFile/testVar126.csv',encoding='gbk')

    cityDict = {}
    with open('../trainFile/cityInformation.csv', 'r') as e:
        for line in e:
            tmpStr = line.strip().replace('： ', ' ').split(' ')
            # for val in tmpStr:
            #     val = val.decode('utf-8')
            cityDict[tmpStr[0]] = tmpStr[1:]

    # print cityDict
    # print cityDict[u'山西'.encode('utf-8')]
    #
    # trainfile = '../trainFile/train.csv'
    # testfile = '../trainFile/test.csv'
    #
    # # trainRetDict = comCityNum(trainfile,cityDict)
    # # testRetDict = comCityNum(testfile,cityDict)
    #
    # trainDF = pd.read_csv(trainfile,encoding='gbk')
    # trainDF['var126'] = trainDF['var126'].fillna(' ')
    # testDF = pd.read_csv(testfile,encoding='gbk')
    # tmpDict = trainDF[['id','var126']].to_dict()
    # for key in xrange(0,24309):
    #     # print type(tmpDict['var126'][key])
    #     # if np.isnan(tmpDict['var126'][key]):
    #     #     print key
    #
    #     tmpls = tmpDict['var126'][key].strip().split('@')
    #     # print tmpDict['var126'][key]
    #     for i in xrange(tmpls.__len__()):
    #         tmpStr = tmpls[i].encode('utf-8').replace(u'市'.encode('utf-8'),'')
    #         if comProvinceNum(cityDict, tmpStr) is None:
    #             print key,tmpStr
        #         if tmpStr == u'长株潭'.encode('utf-8'):
        #             tmpls.remove(tmpStr)
        #             tmpls.extend([u'长沙',u'株洲',u'湘潭'])
        # tmpDict['var126'][key] = '@'.join(tmpls)
        # print tmpDict['var126'][key]

    # print trainRetDict['cityNum']

    #
    # pd.DataFrame(trainRetDict).to_csv('../trainFile/trainCityNumber.csv',index=False)
    # pd.DataFrame(testRetDict).to_csv('../trainFile/testCityNumber.csv',index=False)

    """替换本地 以及数字"""
    # df = pd.read_csv('../trainFile/train.csv', encoding='gbk')
    # # df.var20 = df.var20 + df.var21
    # localCityDict = df.var21.to_dict()
    # replaceLocal('../trainFile/trainVar126.csv','../trainFile/trainVar126New.csv',localCityDict)

    # df = pd.read_csv('../trainFile/test.csv', encoding='gbk')
    # # df.var20 = df.var20 + df.var21
    # localCityDict = df.var21.to_dict()
    # replaceLocal('../trainFile/testVar126.csv','../trainFile/testVar126New.csv',localCityDict)

    df = pd.read_csv('../trainFile/train.csv',encoding='gbk')
    idList = df.id.tolist()
    print idList[0]
    print idList[-1]
    print idList.__len__()

    """处理var126中的城市"""
    result = []
    i = 0
    with open(r'../trainFile/trainVar126Feature.csv','w') as e1:
        e1.write(','.join(['id','provinceNum','cityNum','provinceRate'])+'\n')
        with codecs.open(r'../trainFile/trainVar126New.csv','r','gbk') as e:
            for line in e:
                provinceNum = 0
                cityNum = 0
                tmpLs = set()
                data = line.strip().encode('utf-8').replace(',','@').split('@')[1:]
                for index in xrange(data.__len__()):
                    tmpRes = findCityName(cityDict, data[index])
                    tmpLs.add(tmpRes)
                    # if tmpRes is None:
                        # if data[index] == u'本地'.encode('utf-8'):
                        #     data[index] = localCityDict
                        # print i,':',data[index]
                provinceNum = len(tmpLs)
                cityNum = len(data)
                i += 1
                e1.write(','.join([str(idList[i-1]),str(provinceNum),str(cityNum),str(provinceNum/float(cityNum))])+'\n')
    #
    # replaceSymbol(',@','../trainFile/var126New_2.csv','../trainFile/var126New_3.csv')
    #
    # # checkFile(resLs,'../trainFile/var126New_2.csv','../trainFile/var126.csv','../trainFile/var126New_3.csv')
    # # checkFile([i for i in xrange(23403)],'../trainFile/var126New_1.csv','../trainFile/var126New_2.csv',None)
    #
    #
    # # replaceCityByLine(resLs,'../trainFile/var126New.csv','../trainFile/trainVar126.csv','../trainFile/var126New_1.csv')