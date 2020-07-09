import json
import numpy as np
import pandas as pd

class ConfigProp():

    propHolder = dict()


    def __init__(self, propFile):
        with open(propFile, "r") as prop:
            for line in map(lambda s: s.strip('\n'), prop.readlines()):
                key, value  = map(lambda subs: subs.strip(), line.split('='))
                self.propHolder[key] = value

    def valueForKey(self, key):
        return self.propHolder.get(key, '')

class MegaNumberAnalyzer:

    def __init__(self):
        pass


    def getRepeatedMegaList(self, megaList):
        df = pd.DataFrame(megaList, columns=['seq'])
        repeated_nums = df.pivot_table(index=['seq'], aggfunc='size')
        return list(map(lambda x: x + '(' + str(repeated_nums[x]) + ')*' if x in repeated_nums else x, megaList))



def testConfigProp():
    config = ConfigProp('./properties/config.properties')
    value = config.valueForKey('datafile.shared.basedir')
    print (value)


def test():
    dataDict = {}
    dataDict['n0'] = '23kj'
    dataDict['n1'] = '23kj'
    dataDict['n2'] = '23kj'
    dataDict['n3'] = '23kj'
    dataDict['n4'] = '23kj'

    j = json.dumps(dataDict)
    print (j)
    print(j)

def trueFilePathForKey(configProp: ConfigProp, lotteryType):
    pathWithPlaceholder = configProp.valueForKey('analyzed.data.output.file')
    return pathWithPlaceholder.format(lotteryType=lotteryType)

def printInJson(dictData):

    return json.dumps(dictData)


def testGettingTruePath():
    config = ConfigProp('./properties/config.properties')
    filePath = trueFilePathForKey(config, 'superlotto')
    print(filePath)



if __name__ == '__main__':
    #test()
    #testConfigProp()
    #print(trueFilePath('/Users/michelvu/GeneralStuffs/{lotteryType}/lottoLastResult.txt','superlotto'))
    testGettingTruePath()