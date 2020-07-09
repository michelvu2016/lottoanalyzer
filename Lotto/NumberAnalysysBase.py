import itertools
from  collections import defaultdict
import re
import random


class NumberQuandrantManager:

    def __init__(self):
        self.numberQuadrantMap = defaultdict(lambda : "")


    def add(self, number, quadrantInfo):
        self.numberQuadrantMap[number] = quadrantInfo

    def getQuadrantInfo(self, number):
        return self.numberQuadrantMap.get(number)

class NumberClassMapper:

    ALL_NUMBER_MAP = {
        1 : "01",
        10 : "10",
        20: "20",
        30: "30",
        40: "40",
        50: "50",
        60: "60",
        70: "70"

    }



    def __init__(self):
        self.numberClassMap = {}
        self.numberClassAccumMap = {}

    def clear(self):
        self.numberClassMap = {}

    def map(self, number):
        clsNumber = 0
        tNumber = int(number)
        if tNumber >= 1 and tNumber <= 9:
            clsNumber = 1
        elif tNumber >= 10 and tNumber  <= 19:
            clsNumber = 10
        elif tNumber >= 20 and tNumber <= 29:
            clsNumber = 20
        elif tNumber >= 30 and tNumber <= 39:
            clsNumber = 30
        elif tNumber >= 40 and tNumber <= 49:
            clsNumber = 40
        elif tNumber >= 50 and tNumber <= 59:
            clsNumber = 50
        elif tNumber >= 60 and tNumber <= 69:
            clsNumber = 60
        elif tNumber >= 70 and tNumber <= 79:
            clsNumber = 70


        if not self.numberClassMap.get(clsNumber):
            self.numberClassMap[clsNumber] = 1
        else:
            self.numberClassMap[clsNumber] += 1

    def mapList(self, numberList):
        for num in numberList:
            self.map(num)

    def updateAccum(self):
        for k, v in self.numberClassMap.items():
            if not self.numberClassAccumMap.get(k):
                self.numberClassAccumMap[k] = v
            else:
                self.numberClassAccumMap[k] = self.numberClassMap.get(k) + self.numberClassAccumMap.get(k)

    def _getDisplayStr(self, useTheMap):

        keyList = list(map(lambda k:  k , useTheMap.keys()))
        keyList.sort()

        return " ".join(list(map(lambda n: NumberClassMapper.ALL_NUMBER_MAP.get(n) + "(" + str(useTheMap.get(n)) + ")", keyList)))

    def getDisplayStr(self):
        return self._getDisplayStr(self.numberClassMap)

    def getDisplayForAccumStr(self):
        return self._getDisplayStr(self.numberClassAccumMap)

'''
    Extract the quandrant information from the string
'''
def extractQuadrant(inString):
    pat = re.compile(r'\[\d\]')
    return pat.findall(inString)[0]

def getNumberSetThatNotOverlappedWithDrawnSet(drawnSetList, allDrawnNumber, diplayPickableNumberSetFunc):
    workSet = set()
    for num in allDrawnNumber: #--- copy the whole set
        workSet.update([num])

    #--------- Check to see if the number overlapp ----------
    def checkForMoreThanOneMatch(setToCheck, setListToCheckAgainst):

        validNumber = True

        for num in setListToCheckAgainst:
            if len(setToCheck.intersection(num)) > 1:
                validNumber = False
                break
            else:
                continue

        return validNumber


    def checkPair(accum, allNumberSet):
        if len(allNumberSet) < 2:
            return accum
        num = allNumberSet.pop()
        numberOptForPick = set()
        numberPickForValidating = set([num])

        for numToPair in allNumberSet:
            numberPickForValidating.update([numToPair])
            if not checkForMoreThanOneMatch(numberPickForValidating, drawnSetList):
                numberPickForValidating.remove(numToPair)

            if len(numberPickForValidating) == 5:
                accum.append(numberPickForValidating.copy())
                numberPickForValidating.clear()
                numberPickForValidating.update([num])
        checkPair(accum, allNumberSet)


    listNumberAccum = list()
    checkPair(listNumberAccum, workSet)

    #------------ notify the caller of the result ----
    diplayPickableNumberSetFunc(listNumberAccum)

'''
    Drow the pickable table -------
'''
def getNumberSetThatNotOverlappedWithDrawnSetForPickable(drawnSetList, diplayPickableNumberSetFunc, validateFuncTuple, numberOfSetToGen=10):


    #--------- Check to see if the number overlapp ----------
    def checkForMoreThanOneMatch(setToCheck, setListToCheckAgainst):

        validNumber = True

        for num in setListToCheckAgainst:
            if len(setToCheck.intersection(num)) > 1:
                validNumber = False
                break
            else:
                continue

        return validNumber


    def validateNumSet(testNumSet, allNumberSetList):
        result = True
        for numSet in allNumberSetList:
            if len(testNumSet.intersection(numSet)) > 1:
                result = False
                break

        return result

    '''
        Number set generator
    '''
    def numberSetToGenerateGenerator(allNumberSetList, currentSet):
        workingSet = set()
        workingList = list()

        for numSet in allNumberSetList:
            if (len(numSet.intersection(currentSet))) == 5:
                continue
            workingList.append(list(numSet))

        setIndex = 0
        pivotSetIndex = 0
        for setIndex in range(len(workingList)):
            pivotSet = workingList[setIndex]




        for numIndex in range(5):
            for numInList in workingList:
                workingSet.update([numInList[numIndex]])
            yield workingSet
            workingSet.clear()


    def randomSetGenerator(allNumberSetList, pushFunc):

        done = [False]
        def randomSet():

            selectedSet = random.sample(allNumberSetList, 1)

            return selectedSet

        def controlFunc(stop=False):
            done[0] = stop

        def pickSet():
            pickedSet = set()

            while not done[0]:
                genSet = randomSet()[0]
                num = random.choice(list(genSet))
                pickedSet.update([num])
                if len(pickedSet) == 5:
                    pushFunc(pickedSet, controlFunc)
                    pickedSet = set()

        pickSet()



    def generateNumSet(accum, allNumberSetList):

        pickedSet = set()

        def numberValidationProc(numSet, controlFunc):
            if validateNumSet(numSet, allNumberSetList):
                if validateFuncTuple[1](numSet, validateFuncTuple[0]):
                    accum.append(numSet)

            if len(accum) == numberOfSetToGen:
                controlFunc(stop=True)



        randomSetGenerator(allNumberSetList, numberValidationProc)




    listNumberAccum = list()
    generateNumSet(listNumberAccum, drawnSetList)

    #------------ notify the caller of the result ----

    diplayPickableNumberSetFunc(listNumberAccum)


def filterIfNotOnlyOneNumberAppearInDranSet(drawnSetList, allDrawnNumber):
    numberToBeRemovedSet = set()
    for numSet in drawnSetList:
        numOccurSet = numSet.intersection(allDrawnNumber)
        if len(numOccurSet) > 1:
            numOccurSet.pop()
            numberToBeRemovedSet.update(numOccurSet)

    print ("Number to be removed:", numberToBeRemovedSet)
    numberRemainedSet = allDrawnNumber.difference(numberToBeRemovedSet)

    print ("Number remained:", numberRemainedSet)




'''
    Break down the number set in sort order
'''
def breakDownNumberSetList(numberSetList, processorFunc):

    numberClassMapper = NumberClassMapper()

    for numSet in numberSetList:
        numList = list(numSet)

        numberClassMapper.mapList(numList)
        numList.sort()

        numberClassMapper.updateAccum()
        processorFunc(numList, numberClassMapper.getDisplayStr(), numberClassMapper.getDisplayForAccumStr())
        numberClassMapper.clear()





class NumberAnalysisBase:

    def __init__(self, subclazz):
        self.subclassOfThis = subclazz

    def navigateFile(self, fileName, processorFunc):
        with open(fileName) as inputF:
            for numberLine in list(map(lambda s: s.strip(), inputF.readlines())):
                if numberLine:
                    numbers = numberLine
                    if ";" in numberLine:
                        numbers, mega = numberLine.split(";")
                    processorFunc(set(numbers.split(" ")))

    def removeRepeatedNumberSymbols(self, numberSetPoolToPick):
        return list(map(lambda numset : set(map(lambda num: num[0:2], numset)   ) ,    numberSetPoolToPick       ))


    def checkOverlappedNumbers(self, numSetList, numberSetPicked, processingFunc):
        for numSet in numSetList:
            numSetHasMoreThanOne = numSet.intersection(numberSetPicked)
            if len(numSetHasMoreThanOne) > 1:
                processingFunc(numberSetPicked, numSet,numSetHasMoreThanOne)

    def currentDrawnNumberOverlapping(self, numberSetPoolToPick):

        print ("===================== Last drwan number overlapp check ===============")
        hasOverlappedNumber = False
        def processResult(numberSetIn, numberSetPool, numberSetOverlapped):
            print("***** Drawn set:{}. Past Drawn set {}. overlatpped set {}.".format(numberSetIn, numberSetPool,
                                                                                  numberSetOverlapped))
            hasOverlappedNumber = True

        numSetList = self.removeRepeatedNumberSymbols(numberSetPoolToPick)
        currentDrawnNumberSet = numSetList[0:1][0]
        self.checkOverlappedNumbers(numSetList, currentDrawnNumberSet,  processResult)


    def analyzingPickedNumbers(self, numberSetPoolToPick, lastDrawnNumberList):
        print ("++++++++++++++++ SuperLotto modulating +++++++++++++++++++")
        print("===================== Picked number overlapp check ===============")

        quadrantInfoManager = NumberQuandrantManager()

        numSetList = list(map(lambda numset : set(map(lambda num: num[0:2], numset)   ) ,    numberSetPoolToPick       ))

        allNumberSet = set()
        for numSet in numberSetPoolToPick:
            print (numSet)
            for numberWithData in numSet:
                quadrantInfoManager.add(  numberWithData[0:2]  , extractQuadrant(numberWithData)                 )


            #allNumberSet.update( set(map(lambda snum: snum[0:2], filter(lambda n: "(R)" in n, numSet)  )    ))
            allNumberSet.update(set(map(lambda snum: snum[0:2], filter(lambda n: n, numSet))))

        print (">>All numbers:", allNumberSet)

        def matchOneOfCurrentDrawnList(number):
            return number in lastDrawnNumberList

        def matchOneOfCurrentDrawnListMarker(number):
            if number in lastDrawnNumberList:
                return "**"
            else:
                return ""

        def validEntry(pickableNumerSet, lastDrawnNumberSet):
            return len(pickableNumerSet.intersection(lastDrawnNumberSet)) == 0


        def diplayPickableNumberSet(pickableNumberSet):
            print("====== Pickable List ==========")

            for pNum in pickableNumberSet:
                pnumList = list(pNum)
                pnumList.sort()
                print(   list(  map(lambda n: n+quadrantInfoManager.getQuadrantInfo(n)+ matchOneOfCurrentDrawnListMarker(n), pnumList)  )       )


        getNumberSetThatNotOverlappedWithDrawnSet(numSetList, allNumberSet, diplayPickableNumberSet)

        validateFuncTuple = (set(lastDrawnNumberList), validEntry)
        getNumberSetThatNotOverlappedWithDrawnSetForPickable(numSetList, diplayPickableNumberSet, validateFuncTuple, numberOfSetToGen=700)




        def checkNumber(numberSetPicked):
            #print(numberSetPicked)
            for numSet in numSetList:
                numSetHasMoreThanOne = numSet.intersection(numberSetPicked)
                if len(numSetHasMoreThanOne) > 1:
                    print ("***** Picked set:{}. Drawn set {}. overlatpped set {}.".format(numberSetPicked, numSet, numSetHasMoreThanOne))


        print("++++++++++ Picked number analyzing ++++++++++++")

        self.navigateFile(self.subclassOfThis.pickedFile, checkNumber)


    def dispBreakdownNumberByClass(self, numberSetPoolToPick):

        def displayBreaddownNumberSet(numberList, breakDownString, breakDownAccumString):
            print (numberList, " ----- ["+breakDownString+"]", " ****** ["+breakDownAccumString+"]")


        print (">>>Number list breakdown starts ====")
        breakDownNumberSetList(numberSetPoolToPick, displayBreaddownNumberSet)
        print(">>>Number list breakdown ends ====")