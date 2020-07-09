__author__ = 'michelvu'

import itertools
import re
from  collections import defaultdict
from NumberCheckerOnGroup import NumberCheckerOnGroup

twoDigitsPattern = re.compile(r'(\d\d)')




def numberInsetOutsideOfRange(numberset=None, numRange=None, checknumber=None):
    if testSet is None or numRange is None:
        return
    numList = [x for x in testSet]
    result = filter(lambda x: not (x < checknumber - numRange or x > checknumber + numRange), numList)

    return len([x for x in result])

#numberInRange = numberInsetOutsideOfRange(numberset=testSet, numRange=5, checknumber=2)

def one():
    print ("One")

def two():
    print ("two")


def combo():
    return one, two


def testPaddingNumberString():

    myList = list(map(lambda i: ("0" + str(i))[0:] if i < 10 else str(i), list(range(1, 56))))

    print(myList)

def testPaddingNumberWithDelta():
    number = '15'
    delta = -1
    print(('0' + str(int(number) + delta))[-2:])

def FormatNumberList(numberList):

    formattedList = "'"+ "{:<10}" * len(numberList) + "'"+  ".format("+ ",".join(   map(lambda s: "'" + s + "'", numberList)        )          +")"
    return (eval(formattedList))


def fornatNumberListUsingPrint():
    numberList = '01(R+)', '16(R-)', '17(R)', '19', '10'


def flatList():
    ta = [[1,2,3,4], [4,5,6],[6,7,8]]
    print (list(itertools.chain(*ta)))


def sliceList():
    listOfList = [
        list(['01', '11', '15', '35', '31']),
        list(['02', '11', '15', '35', '31']),
        list(['03', '11', '15', '35', '31']),
        list(['04', '11', '15', '35', '31']),
        list(['05', '11', '15', '35', '31']),
        list(['06', '11', '15', '35', '31']),
        list(['07', '11', '15', '35', '31']),
    ]

    print (listOfList[1:])


def setPair():
    testSet = set(["02", "03"])
    print (testSet)
    testSet.remove("03")
    print (testSet)

    myList  = list()


def extractQuadrant():
    testS = '39(R-)[2]'
    pat = re.compile(r'\[\d\]')
    print (pat.findall(testS)[0])

    testD = defaultdict(lambda : list())

    testD['ba'] = "Be"

    print (testD["ba"])


def testSet():
    tset = set()
    tlist = list()

    tset.update(['02'])
    tset.update(['23'])
    tset.update(['34'])

    tlist.append(list(tset))


    print (tlist)

    for numIndex in range(5):
        print (numIndex)

def selectDigit(entry):

    founds = twoDigitsPattern.findall(entry)
    return founds[0]

def cleanUpNumberPickList():


    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:



        filteredLines = list(map(lambda ts: ts.rstrip(), filter(lambda s: '**' not in s, inputF.readlines())))
        filteredLines.sort()
        for l in filteredLines:
            nList = list(map(lambda s: selectDigit(s), l.split(",")))
            nList.sort()
            print (nList)

def filterSelection():

    twoDigitsPattern = re.compile(r'(\d\d)')
    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:
        filteredLines = list(map(lambda ts: ts.rstrip(), filter(lambda s: '*' in s, inputF.readlines())))

        for l in filteredLines:
            nList = list(map(lambda s: selectDigit(s), l.split(",")))
            nList.sort()
            print (nList)





twoDigitsPattern = re.compile(r'(\d\d)')




def numberInsetOutsideOfRange(numberset=None, numRange=None, checknumber=None):
    if testSet is None or numRange is None:
        return
    numList = [x for x in testSet]
    result = filter(lambda x: not (x < checknumber - numRange or x > checknumber + numRange), numList)

    return len([x for x in result])

#numberInRange = numberInsetOutsideOfRange(numberset=testSet, numRange=5, checknumber=2)

def one():
    print ("One")

def two():
    print ("two")


def combo():
    return one, two


def testPaddingNumberString():

    myList = list(map(lambda i: ("0" + str(i))[0:] if i < 10 else str(i), list(range(1, 56))))

    print(myList)

def testPaddingNumberWithDelta():
    number = '15'
    delta = -1
    print(('0' + str(int(number) + delta))[-2:])

def FormatNumberList(numberList):

    formattedList = "'"+ "{:<10}" * len(numberList) + "'"+  ".format("+ ",".join(   map(lambda s: "'" + s + "'", numberList)        )          +")"
    return (eval(formattedList))


def fornatNumberListUsingPrint():
    numberList = '01(R+)', '16(R-)', '17(R)', '19', '10'


def flatList():
    ta = [[1,2,3,4], [4,5,6],[6,7,8]]
    print (list(itertools.chain(*ta)))


def sliceList():
    listOfList = [
        list(['01', '11', '15', '35', '31']),
        list(['02', '11', '15', '35', '31']),
        list(['03', '11', '15', '35', '31']),
        list(['04', '11', '15', '35', '31']),
        list(['05', '11', '15', '35', '31']),
        list(['06', '11', '15', '35', '31']),
        list(['07', '11', '15', '35', '31']),
    ]

    print (listOfList[1:])


def setPair():
    testSet = set(["02", "03"])
    print (testSet)
    testSet.remove("03")
    print (testSet)

    myList  = list()


def extractQuadrant():
    testS = '39(R-)[2]'
    pat = re.compile(r'\[\d\]')
    print (pat.findall(testS)[0])

    testD = defaultdict(lambda : list())

    testD['ba'] = "Be"

    print (testD["ba"])


def testSet():
    tset = set()
    tlist = list()

    tset.update(['02'])
    tset.update(['23'])
    tset.update(['34'])

    tlist.append(list(tset))


    print (tlist)

    for numIndex in range(5):
        print (numIndex)

def selectDigit(entry):

    founds = twoDigitsPattern.findall(entry)
    return founds[0]

def cleanUpNumberPickList():


    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:



        filteredLines = list(map(lambda ts: ts.rstrip(), filter(lambda s: '**' not in s, inputF.readlines())))
        filteredLines.sort()
        for l in filteredLines:
            nList = list(map(lambda s: selectDigit(s), l.split(",")))
            nList.sort()
            print (nList)

def filterSelection():

    twoDigitsPattern = re.compile(r'(\d\d)')
    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:
        filteredLines = list(map(lambda ts: ts.rstrip(), filter(lambda s: '*' in s, inputF.readlines())))

        for l in filteredLines:
            nList = list(map(lambda s: selectDigit(s), l.split(",")))
            nList.sort()
            print (nList)

def selectNumberBasedOnQuadran():

    pickPattern = [
        re.compile(r'\[2\]'),
        re.compile(r'\[2\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[4\]')]

    numberMatchPattern = re.compile(r'(\d\d)')

    numberCheckerOnGroup = NumberCheckerOnGroup()

    numberCheckerOnGroup.setGroup((1,20,20,30,40))

    def matchPattern(line):
        retValue = True
        for pattern in pickPattern:
            if pattern.findall(line):
                continue
            else:
                retValue = False
                break
        return retValue

    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:
        filteredLines = list(map(lambda ts: ts.rstrip(), inputF.readlines()))

        for l in filteredLines:
            if matchPattern(l):
                number = list(map(lambda n: int(n), numberMatchPattern.findall(l)))
                if numberCheckerOnGroup.matchGroup(number):
                    print (number)


def cleanUpNumberSet():
    numberSet = \
    """['41[2]', '10[3]', '27[3]', '37[3]', '13[3]']
['26[4]', '12[4]', '10[3]', '38[3]', '06[3]']
['41[2]', '10[3]', '27[3]', '37[3]', '13[3]']
['03[2]', '27[3]', '33[4]', '22[1]', '46[3]']
['26[4]', '10[3]', '32[4]', '20[2]', '37[3]']"""


    listAllNum = re.compile(r'\d{2}').findall("".join(numberSet.split("\n"))  )
    line = list()
    for num in listAllNum:
        line.append(num)
        if len(line) == 5:
            print (" ".join(line))



            line.clear()


def testDefaultdict():

    def handleMissingEntry(*args, **kwargs):
        print (args, kwargs)

    myMap = defaultdict(handleMissingEntry)

    myMap['a'] = 1
    myMap['b'] = 2

    myOtherMap = {}
    myOtherMap['a'] = 3



    print (myOtherMap)





def cleanUpNumberPickListckList():

    pickPattern = [
        re.compile(r'\[2\]'),
        re.compile(r'\[2\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[4\]')]


    def matchPattern(line):
        retValue = False
        for pattern in pickPattern:
            if pattern.match(line):
                continue
        return retValue

    with open (r'numberValidation/pickList.txt', mode='rt') as inputF:
        filteredLines = list(map(lambda ts: ts.rstrip(), inputF.readlines()))

        for l in filteredLines:
            if matchPattern(l):
                print (l)


def cleanUpNumberSet():
    numberSet = \
    """['41[2]', '10[3]', '27[3]', '37[3]', '13[3]']
['26[4]', '12[4]', '10[3]', '38[3]', '06[3]']
['41[2]', '10[3]', '27[3]', '37[3]', '13[3]']
['03[2]', '27[3]', '33[4]', '22[1]', '46[3]']
['26[4]', '10[3]', '32[4]', '20[2]', '37[3]']"""


    listAllNum = re.compile(r'\d{2}').findall("".join(numberSet.split("\n"))  )
    line = list()
    for num in listAllNum:
        line.append(num)
        if len(line) == 5:
            print (" ".join(line))



            line.clear()


def testDefaultdict():

    def handleMissingEntry(*args, **kwargs):
        print (args, kwargs)

    myMap = defaultdict(handleMissingEntry)

    myMap['a'] = 1
    myMap['b'] = 2

    myOtherMap = {}
    myOtherMap['a'] = 3



    print (myOtherMap)


def minusOneToSet():
    test = set(['01', '05', '12', '14', '38'])
    addOne = set(map(lambda x: '0' + str(  int(x) - 1) if int(x) < 10 else  str(int(x)), test))

    print(addOne)


def addOneToSet():
    test = set(['01', '09', '12', '14', '38'])
    addOne = set(map(lambda x: '0'+str(int(x)+1) if int(x) < 9 else  str(int(x)+1)    , test))

    print (addOne)


def formatNumber(numStr):
    pass

#print (numberInRange)
#print (sum([44.16 * 7]))


#combo()[0]()

#testPaddingNumberWithDelta()


#flatList()

#sliceList()

#setPair()

##extractQuadrant()

#testSet()

#cleanUpNumberSet()

#cleanUpNumberPickList()

#testDefaultdict()

#filterSelection()
#selectNumberBasedOnQuadran()

#addOneToSet()
