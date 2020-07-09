__author__ = 'michelvu'

import itertools
import re
from  collections import defaultdict
from NumberCheckerOnGroup import NumberCheckerOnGroup

twoDigitsPattern = re.compile(r'(\d\d)')











twoDigitsPattern = re.compile(r'(\d\d)')






def selectNumberBasedOnQuadran(matchQuadantTuple, lastDrawn=None, checkRule=None):

    pickPattern = [
        re.compile(r'\[2\]'),
        re.compile(r'\[2\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[3\]'),
        re.compile(r'\[4\]')]

    numberMatchPattern = re.compile(r'(\d\d)[\[](\d)')

    numberCheckerOnGroup = NumberCheckerOnGroup()

    numberCheckerOnGroup.setGroup((1,20,20,30,40))

    matchQuadantTupleList =  list(map(lambda n: str(n), matchQuadantTuple))

    print (matchQuadantTupleList)

    def matchPattern(line):
        retValue = True
        for pattern in pickPattern:
            if pattern.findall(line):
                continue
            else:
                retValue = False
                break
        return retValue

    def matchQuadrant(numberList):
        quadrantCheck = set();

        for quadNum in matchQuadantTupleList:
            for number in numberList:
                if number[1] == quadNum:
                    if not number[0] in quadrantCheck:
                        quadrantCheck.add(number[0])
                        break

        return len(quadrantCheck) == 5


    def makeMatchTupble(numberQuadset):
        matchNum = numberMatchPattern.findall(numberQuadset)
        #print (matchNum[0])
        return [matchNum[0][0], matchNum[0][1]]

    def acceptable(number, checkRule):
        numberSet = set(number)
        return (not len(numberSet.intersection(lastDrawn))) and (checkRule(numberSet, lastDrawn) if checkRule else True)

    print ("last drawn number:", lastDrawn)

    with open (r'numberValidation/pickableList.txt', mode='rt') as inputF:
        filteredLines = list(map(lambda ts: ts.rstrip(), inputF.readlines()))

        for l in filteredLines:
            number = list(map(lambda x: makeMatchTupble(x), l.split(",")))
            #print (number)
            if matchQuadrant(number):
                eligibleNumber = list(map(lambda n: n[0], number))
                if(acceptable(eligibleNumber, checkRule)):
                    print (eligibleNumber)

def minusOneToSet(mySet):

    minusOne = set(map(lambda x: '0' + str(  int(x) - 1) if int(x) < 10 else  str(int(x)-1), mySet))

    return minusOne


def addOneToSet(mySet):

    addOne = set(map(lambda x: '0'+str(int(x)+1) if int(x) < 9 else  str(int(x)+1)    , mySet))

    return addOne

def rule_noImmediateAdjacent(pickedNumSet, lastDrawnSet):
    addOneDrawnSet = addOneToSet(lastDrawnSet)
    minusOneDrawnSet = minusOneToSet(lastDrawnSet)
    matchedAddOneOrMinusOne =  (pickedNumSet.intersection(addOneDrawnSet) or pickedNumSet.intersection(addOneDrawnSet))
    return not matchedAddOneOrMinusOne

def formatNumber(numberString):
    return re.findall(r'(\d\d)', numberString)


currentDrawnNumbers = "2403361512"

selectNumberBasedOnQuadran(
    (1,2,3,4,4),set(formatNumber(currentDrawnNumbers)), None

)




