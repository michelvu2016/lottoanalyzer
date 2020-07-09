__author__ = 'michelvu'

import os
import sys

import re, random
from random import randrange
import itertools
from NumberAnalyzer import Fantasy5Analysis, MegaMillionAnalysis, SuperLottoAnalysis, PowerBallAnalysis
from utils import tools
import LottoUtils as myUtils
from LottoUtils import ConfigProp, MegaNumberAnalyzer


resultDataDict = dict()
lotteryType = ''
configProp = ConfigProp('./properties/config.properties')
megaNumberAnalyzer = MegaNumberAnalyzer()

class LottoNumbers:


    availableSymbolList = [c for c in "!@#$%^&*()-+~<>qwertyuiopasdfghjklzxcvbnmå"]

    def __init__(self):
        self.pastNumbers = []
        self.mega = []
        self.numTickets = 1
        self.depthDraw = 25
        self.startFrom = 3
        self.depthDrawForMega = 9;
        self.numberFromForwardList=1
        self.numberFromBackardList=3
        self.poolNumberSet = set()
        self.numberRangeSet=None
        self.numberDistanceFromCurrentPickedNumber=0
        self.repeatedNumberStat = {}
        self.pastDrawnNumberSet = set()
        self.repeatedNumberWithinLastDrawnNumberSetMap = {}
        self.analyzingEngine = Fantasy5Analysis()


    def setNumTicket(self, numtickets):
        self.numTickets = numtickets



    def setNumberRange(self, startnum, endnum):
        if range is not None:
            self.numberRangeSet = set(map(lambda i: ("0"+ str(i))[0:] if i < 10 else str(i)  ,list(range(startnum,  endnum))))

    def addNumber(self, numberSeq = None):
        if numberSeq is None:
            return
        numList = []
        for x in range(9):
             if x % 2 == 0:
                delta = 2 if x == 0 else x + 2
                numList.append(numberSeq[x:delta])
        self.pastNumbers.append(set(numList))


    def addMega(self, megaNumber=None):
        if megaNumber is None:
            return

        self.mega.append('0' + megaNumber if len(megaNumber) == 1 else megaNumber )


    def drawNumbers(self):
        numSet1, numSet2 = self.pastNumbers[2:4]

        for numSetSample in self.pastNumbers:
            matchNumSet1 = numSet1.intersection(numSetSample)
            matchNumSet2 = numSet2.intersection(numSetSample)
            print (matchNumSet1, matchNumSet2)


    def genNumberSample(self):
        for sampleNums in self.pastNumbers:
            print (sampleNums)
            yield sampleNums

    '''
        function to validate the input number set to see if it collide with the latest
        drawn numbers
    '''
    def validatePickedNumber(self, pickednumberlistTuple=None, numberofpastnumdrawn=None, numberofpastmegadrawn=None):
        megaDrawn = None
        numberDrawn = None

        if numberofpastmegadrawn is not None:
            megaDrawn = self.mega[0:numberofpastmegadrawn]

        if numberofpastnumdrawn is not None:
            numberDrawn = self.pastNumbers[0:numberofpastnumdrawn] #numberDrawn = list[set[list[number]]]]

        print ("======  Picked number analysis =============")
        print("last drawn number sets:")
        for num in self.pastNumbers[0:5]:
            print (num)

        if megaDrawn:
            print ("last Mega drawn:", megaDrawn)

        def numberSetByDelta(currSet=None, delta=None):
            newSet = set(map(lambda x: ('0'+ str(int(x) + delta))[1:], currSet ))
            return newSet

        lineCount = 0
        for numbers, mega in pickednumberlistTuple:
            if numbers is not None:
                pickedNumberSet = set(numbers)
                numberIsOk = True
                megaIsOk = True

                result = None
                lineCount = lineCount + 1
                for numSet in numberDrawn:

                    matchedExactSet = pickedNumberSet.intersection(numSet)
                    matchedOnePlusSet = pickedNumberSet.intersection(numberSetByDelta(numSet,1))
                    matchedOneMinusSet = pickedNumberSet.intersection(numberSetByDelta(numSet, -1))

                    displayNumbers = numbers

                    if matchedExactSet:
                        displayNumbers = map(lambda n: n+"(M)" if n in matchedExactSet else n, displayNumbers)
                        numberIsOk = False

                    if matchedOnePlusSet:
                        displayNumbers = map(lambda n: n+"(NU)" if n in matchedOnePlusSet else n, displayNumbers)
                        numberIsOk = False

                    if  matchedOneMinusSet:
                        displayNumbers = map(lambda n: n+"(NL)" if n in matchedOneMinusSet else n, displayNumbers)
                        numberIsOk = False

                    displayNumbers = set(displayNumbers)
                    displayRec = ["{}.".format(lineCount)]
                    if mega is not None:
                        if str(int(mega)) in megaDrawn:
                            displayRec.append(("Mega {} is not Ok.".format(mega)))
                        else:
                            displayRec.append(("Mega {} is Ok.".format(mega)))

                    if not numberIsOk:
                        displayRec.append(("Number {} is not Ok.".format(displayNumbers)))
                        def redrawNumber(ticket):
                            displayRec.append(("New ticket {} *****".format(" ".join(map(lambda s: "0"+s if len(s) == 1 else s,  ticket  )    ))))
                        self.drawTicket(numberOfTicketToDraw=1, reportResultToFunc=redrawNumber)

                    else:
                        displayRec.append(("Number {} is Ok.".format(displayNumbers)))

                    if displayRec:
                        print (" ".join(displayRec))

    def repeateNumberStatCalc(self, repNumberSet):
        for n in repNumberSet:
            if self.repeatedNumberStat.get(n):
                self.repeatedNumberStat[n] = self.repeatedNumberStat.get(n)+1
            else:
                self.repeatedNumberStat[n] = 1

    def genNumber(self):
        repeatedNumbers = set()

        selNumberSet = self.pastNumbers[self.startFrom:self.depthDraw]

        #--- Find the repeated number in setNummberSet ----

        allUniqueNumbersSet = set()

        for numberSet in selNumberSet:
            allUniqueNumbersSet.update(numberSet)
            for numberSetinPast in selNumberSet:
                matchNumberSet = numberSet.intersection(numberSetinPast)
                if matchNumberSet == numberSet:
                    continue
                else:
                    repeatedNumbers.update(matchNumberSet)
                    self.repeateNumberStatCalc(matchNumberSet)


        print (r"===== None repeated numbers")
        print(list(filter(lambda n: n not in repeatedNumbers, allUniqueNumbersSet)))

        if(len(repeatedNumbers)):

            def inRangeOfNumberToPick(num):

                return num > 0 or ('0' + str(num))[-2:] in self.numberRangeSet

            def repeatedNumberWithDelta(repNumbers, delta):
                return list(filter (lambda num : num not in repeatedNumbers,
                             map( lambda n: ('0'+str(int(n) + delta))[-2:] if inRangeOfNumberToPick(int(n)+delta) else ('0'+str(int(n)))[-2:] , repeatedNumbers)))


            #print (repeatedNumbers)
            print ("====== Repeated numbers:")
            self.printListNumber(  sorted(repeatedNumbers) )
            print ("====== Repeated number plus one:")
            self.printListNumber(sorted(repeatedNumberWithDelta(repeatedNumbers, 1)))

            print ("====== Repeated number minus one:")
            self.printListNumber(sorted(repeatedNumberWithDelta(repeatedNumbers, -1)))

            self.poolNumberSet = repeatedNumbers

            electedTicket = self.drawTicket()
            if len(self.mega):
                self.drawMega()
            #----- Output the jason data file -----------
            self.outputResultInJasonToFile()

    def printListNumber(self, numberList):

        inList = list(numberList)
        plist = inList[0:20];

        print (plist)
        plist = inList[21:]
        print (plist)


    def shuffleBucket(self, bucketNumbers):
        useBucket = bucketNumbers
        for x in range(randrange(1, 10)):
            random.shuffle(useBucket)

        return useBucket;

    def drawTicket(self, numberOfTicketToDraw=None, reportResultToFunc=None ):

        def numberSetByDelta(currSet=None, delta=None):
            newSet = set(map(lambda x: ('0'+ str(int(x) + delta))[1:] if x != "01" and x != "69" else x, currSet ))
            return newSet

        numberInPool = len(self.poolNumberSet)
        elibibleNumbers = list(self.poolNumberSet)

        elibibleNumbersPlus = list(numberSetByDelta(currSet=self.poolNumberSet, delta=1))
        elibibleNumbersMinus = list(numberSetByDelta(currSet=self.poolNumberSet, delta=-1))

        poolNumberManager = {}

        self.pastDrawnNumberSet = self.pastNumbers[0:30]

        if self.numberFromBackardList:
            for i in range(0, self.numberFromBackardList):
                poolNumberManager[i] = elibibleNumbersMinus

        nextIndex = len(poolNumberManager)
        if self.numberFromForwardList:
            for i in range(nextIndex, self.numberFromForwardList+nextIndex):
                poolNumberManager[i] = elibibleNumbersPlus

        ticket = set()
        lastDrawnNumbers = self.pastNumbers[0]
        #print (">>>Last drawn number: ", lastDrawnNumbers)

        if reportResultToFunc is None:
            self.printLastDrawnNumbers(lastDrawnNumbers, self.poolNumberSet)

        if numberOfTicketToDraw is None:
            numberOfTicketToDraw = self.numTickets

        def inAnyPastDrawnNumberSet(proposedNumber):
            for drnNumSet in self.pastDrawnNumberSet:
                return ('0'+str(int(proposedNumber)))[-2:] in drnNumSet

        def genNumberSet(numberOfTicketToDraw, numbersToPickFrom):
            newTicket = set()

            while(True):

                numberPoolToPick = numbersToPickFrom
                numberPoolToPick = self.shuffleBucket( poolNumberManager.get((len(ticket)), numberPoolToPick))
                pickedNumber = random.sample(numberPoolToPick,1)[0]
                if pickedNumber in lastDrawnNumbers or inAnyPastDrawnNumberSet(pickedNumber):
                    continue

                if self.numberDistanceFromCurrentPickedNumber and \
                        isNumberInsetInsideOfRange(numberset=ticket, numRange=self.numberDistanceFromCurrentPickedNumber, checknumber=pickedNumber):
                    continue

                newTicket.add(pickedNumber)
                if(len(newTicket) >= 5):
                    return newTicket

        for x in range(numberOfTicketToDraw):
            ticket = genNumberSet(self.numTickets, elibibleNumbers)
            ticketFromRandomPick = genNumberSet(self.numTickets, list(self.numberRangeSet))

            #numbersForTicket = random.sample(elibibleNumbers, 5)
            if reportResultToFunc is not None:
                reportResultToFunc(ticket)
            else:
                print("Number from repeated set:{} - Number from randome pick:{}".format(ticket, ticketFromRandomPick))



        ticket.clear()

    def matchLast2Draws(self):

        pastGameStartAt = 10
        passedPercentage = 60

        def flatList(inList):
            return list(itertools.chain(*inList))

        def next3GrameFrom(startFrom):
            last3games = self.pastNumbers[startFrom-3: startFrom][::-1]
            return last3games

        def last2drawnNumberSet():
            return self.pastNumbers[:2]

        def numberMatchedInLists(list1, list2):
            return list(filter(lambda n: n in list1, list2))

        def percentageOfMatch(numberMatch, totalNumber):
            return (numberMatch * 100) / totalNumber

        topDrawnGames = flatList(last2drawnNumberSet())

        while pastGameStartAt <= 21:

            next3Games = flatList(next3GrameFrom(pastGameStartAt))
            matchedList =  numberMatchedInLists(topDrawnGames, next3Games)

            print ("top 2 drawn:", topDrawnGames)
            print ("Next 3 games:", next3Games)
            print ("Matched List:", matchedList)
            print ("Percentage matched: ", percentageOfMatch(len(set(matchedList)), 5))

            pastGameStartAt += 3


    def printTickets(self, ticket):
        print (" ".join(ticket))

    def printLastDrawnNumbers(self, lastDrawnNumberList, repeatedNumber):



        def nearMatchRepeatedNumbers(number):
            if number == "01":
                return number
            else:
                for delta, symbol in {1: "R-",-1:"R+"}.items():
                    if ('0' + str(int(number) + delta))[-2:] in repeatedNumber:
                        return number + "("+symbol+")"
                    else:
                        continue
                return number

        def repeatedNumberValidation(number, repeatedNumbersIn):
            if number in repeatedNumbersIn:
                return True
            else:
                return False

        def numberRepeatedWithinPastDraws(drawnNumber):
            matchInSetSymbol = ""
            if self.repeatedNumberWithinLastDrawnNumberSetMap.get(drawnNumber):
                return self.repeatedNumberWithinLastDrawnNumberSetMap.get(drawnNumber)

            for numdrnSet in self.pastDrawnNumberSet:
                if drawnNumber in numdrnSet:
                    matchInSetSymbol = LottoNumbers.availableSymbolList.pop()
                    self.repeatedNumberWithinLastDrawnNumberSetMap[drawnNumber] = matchInSetSymbol
                    break
            return matchInSetSymbol




        def repetitionRate(num):
            if self.repeatedNumberStat.get(num):
                return str(self.repeatedNumberStat.get(num))
            else:
                return ""

        def matchOneOfCurrentDrawnList(number):
            if number in lastDrawnNumberList:
                return "**"
            else:
                return ""

        def numberListWithAnalysisInfo(numberIter, repeatedNumbers):
            selNumberList = list(
                map(lambda n: n + '(R)'+repetitionRate(n)+numberRepeatedWithinPastDraws(n)+matchOneOfCurrentDrawnList(n) if repeatedNumberValidation(n, repeatedNumbers) else nearMatchRepeatedNumbers(n) + matchOneOfCurrentDrawnList(n), numberIter))
            return selNumberList

        def FormatNumberList(numberList):

            formattedList = "'" + "{:<15}" * len(numberList) + "'" + ".format(" + ",".join(
                map(lambda s: "'" + s + "'", numberList)) + ")"
            return (eval(formattedList))


        self.matchLast2Draws()

        selNumberList =   numberListWithAnalysisInfo(lastDrawnNumberList, repeatedNumber)   #list(map(lambda n: n + '(R)' if n in repeatedNumber else nearMatchRepeatedNumbers(n), lastDrawnNumberList))
        print (">>>Last drawn number:"," ".join(selNumberList))

        print (">>>Past drawn numbers:")
        lineNumber = 0;

        quadrantIndex = 1
        numberSetListWithAnalysis = []
        resultDataDict['lastDrawnNumberList'] = selNumberList
        for number in self.pastDrawnNumberSet[1:]:
            numberListWithAnalysis = numberListWithAnalysisInfo(number, repeatedNumber)

            numberSetListWithAnalysis.append(list(map(lambda snum: snum+"["+str(quadrantIndex)+"]", numberListWithAnalysis)))

            numberListWithBreakdownInfo = numberListWithAnalysisInfo(number, repeatedNumber)

            resultDataDict['numLine'+str(lineNumber)] = numberListWithBreakdownInfo
            print(FormatNumberList(numberListWithAnalysisInfo(number, repeatedNumber)))

            lineNumber += 1
            if lineNumber % 5 == 0:
                print ("===============Quad================================================")
                quadrantIndex += 1

        uSet = self.displayUniqueNumberForAllQuadrands(self.pastDrawnNumberSet)

        self.displayGapInSelectedNumberSet(uSet)

        #self.analyzingEngine.analyzingPickedNumbers(numberSetListWithAnalysis, lastDrawnNumberList)
        self.analyzingEngine.currentDrawnNumberOverlapping(numberSetListWithAnalysis)

        self.analyzingEngine.dispBreakdownNumberByClass(self.pastDrawnNumberSet)

    def outputResultInJasonToFile(self):
        print("======  Display result in Json ========")
        dataInJason = myUtils.printInJson(resultDataDict)
        print (dataInJason)
        targetOutFilePath = myUtils.trueFilePathForKey(configProp, lotteryType)
        with open(targetOutFilePath, "w") as lottoResult:
            lottoResult.write(dataInJason)
        print("======  end Display result in Json ========")


    def displayUniqueNumberForAllQuadrands(self, numberSet):
        print ("*** Unique number in set:")
        uSet = tools.toUniqueSet(numberSet)
        tools.listWrapper(uSet, 12, lambda x: print(x))
        return uSet


    def displayGapInSelectedNumberSet(self, numberSet):
        print ("*** Number in the gap:")
        print(tools.gapNumbersInSet(numberSet))



    def drawMega(self):

        print(' '.join(self.mega))
        numberInPool = len(self.mega)

        analyzedMegaList = megaNumberAnalyzer.getRepeatedMegaList(self.mega)

        megaPool = analyzedMegaList[:self.depthDrawForMega]

        print(' '.join(megaPool))

        repeatedMegaNumber = set()
        megaSamplerSet = set()





        firstNumber = True
        for megNum in megaPool:
            if firstNumber:
                megaSamplerSet.add(megNum)
                firstNumber = False
                continue
            if megNum in megaSamplerSet:
                repeatedMegaNumber.add(megNum)
            else:
                megaSamplerSet.add(megNum)

        def matchRepeatedMega(megNum):
            return megNum in repeatedMegaNumber

        # last125Mega = list(map(lambda n: n+"*" if matchRepeatedMega(n) else n, megaPool[0:25]))
        # print(">>>Last 25 mega numbers: ", last125Mega)

        megaResultDict = dict()
        def megaInJson(key, numberList):
            megaResultDict[key] = list(numberList)

        self.displayLastMegaNumber(megaPool, repeatedMegaNumber, 25, megaInJson)
        self.displayLastMegaNumber(megaPool, repeatedMegaNumber, 40, megaInJson)
        megaInJson("repeatedMega", repeatedMegaNumber)

        print ("Repeated mega:",repeatedMegaNumber)
        for x in range(self.numTickets):
            numbersForTicket = random.sample(repeatedMegaNumber, 1)
            print (numbersForTicket)

        resultDataDict['megaResult'] = megaResultDict


    def displayLastMegaNumber(self, megaPool, repeatedMegaSet, numberOfElms, processorFunc):

        def matchRepeatedMega(megNum):
            return megNum in repeatedMegaSet

        last125Mega = list(map(lambda n: n + "*" if matchRepeatedMega(n) else n, megaPool[0:numberOfElms]))

        print(">>>Last ",numberOfElms," mega numbers:")

        processorFunc(f'last{numberOfElms}mega', last125Mega)

        tools.listWrapper(last125Mega, 15, lambda l: print(l))





def isNumberInsetInsideOfRange(numberset=None, numRange=None, checknumber=None):
    if numberset is None or numRange is None or checknumber is None:
        return False
    if not len(numberset):
        return False
    invalid = False
    for x in numberset:
        testx = int(x)
        pickedNumber = int(checknumber)
        invalid = abs(testx - pickedNumber) < numRange
        if invalid:
            break
    return invalid


def getNumber(numberFileName, regExp=None):
    numberList = []
    #"Oct 21, 2015 - 265	5732304256	11"


    ##numberFormatReg = r'^([A-Za-z]{3})'
    ##numberFormatReg = r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3})'
    numberFormatReg = r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3,5})\s([\d]{10})\s([\d]{1,2})'
    if regExp is not None:
        numberFormatReg = regExp
    pastNumbers = LottoNumbers()

    matchPattern = re.compile(numberFormatReg)
    numberIndex = 0
    numGameGoBack = 16
    startGame = 8
    with open(numberFileName) as inputFile:
        '62', '8', '25', '23', '74'
        for line in inputFile:
            textLine = line.strip("\r\n")
            if len(textLine) < 5:
                continue
            numberIndex += 1
            lottoMega= None
            #if startGame <=  numberIndex <= startGame+numGameGoBack:
            entry = matchPattern.findall(textLine)[0]
            if len(entry) == 4:
                lottoDate, lottoSeq, lottoNumber, lottoMega = entry
            else:
                lottoDate, lottoSeq, lottoNumber = entry
            pastNumbers.addNumber(lottoNumber)

            if lottoMega is not None:
                pastNumbers.addMega(lottoMega)


    return pastNumbers


def genPowerBall(callbackFunct, regExp=None, numTickets=2, depth=120, startFrom=2, depthForMega=10):

    print ("=========== Powerball ===========================")

    baseDir = configProp.valueForKey('datafile.shared.basedir')
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_powerball.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    pastNumbers.setNumberRange(1, 69)
    pastNumbers.analyzingEngine = PowerBallAnalysis()
    callbackFunct(pastNumbers)
    return pastNumbers

def genMegaMil(callbackFunct, regExp=None, numTickets=5, depth=25, startFrom=2,depthForMega=50):

    print ("=========== Megamillion ===========================")

    baseDir = configProp.valueForKey('datafile.shared.basedir')
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_megamillion.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    pastNumbers.setNumberRange(1,70)
    pastNumbers.analyzingEngine = MegaMillionAnalysis()
    callbackFunct(pastNumbers)
    return pastNumbers


def genSuperLotto(callbackFunct, regExp=None, numTickets=5, depth=25, startFrom=2,depthForMega=10):

    print ("=========== Superlotto ===========================")

    baseDir = configProp.valueForKey('datafile.shared.basedir')

        #"/Users/michelvu/Python/Learning/Lotto/data/"
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_superlotto.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    pastNumbers.setNumberRange(1,47)
    pastNumbers.analyzingEngine = SuperLottoAnalysis()
    callbackFunct(pastNumbers)
    return pastNumbers


def fantasy5(callbackFunct, regExp=None, numTickets=4, depth=50, startFrom=2, depthForMega=10):

    print ("=========== Fantasy 5 ===========================")

    baseDir = configProp.valueForKey('datafile.shared.basedir')
    pastNumbers = getNumber("{}{}".format(baseDir, "fantasy5.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDraw = depth
    pastNumbers.setNumberRange(1, 39)
    pastNumbers.depthDrawForMega = depthForMega
    pastNumbers.analyzingEngine = Fantasy5Analysis()
    callbackFunct(pastNumbers)
    return pastNumbers



def validateSuperLottoNumber(callbackFunct,pastNumbers):
    print ("======== Super Lotto Pcked Number validation =========")
    pickednumfile = "numberValidation/superLottoPicked.txt"
    drawnnumberfile = "numbers_superlotto.txt"
    validatePickedNumbers(callbackFunct, pickednumfile=pickednumfile, pastNumbers=pastNumbers)


def validateMegaMillionNumber(callbackFunct,pastNumbers):
    print ("======== Mega Million Pcked Number validation =========")
    pickednumfile = "numberValidation/megamillionPicked.txt"
    drawnnumberfile = "numbers_megamillion.txt"
    validatePickedNumbers(callbackFunct, pickednumfile=pickednumfile, pastNumbers=pastNumbers)


def validatePowerballNumber(callbackFunct, pastNumbers):
    print ("======== Powerball Pcked Number validation =========")
    pickednumfile = "numberValidation/PowerballPicked.txt"
    drawnnumberfile = "numbers_powerball.txt"
    validatePickedNumbers(callbackFunct, pickednumfile=pickednumfile, pastNumbers=pastNumbers)

def validateFantasy5Number(callbackFunct, pastNumbers):
    print("======== Fantasy 5 Pcked Number validation =========")
    pickednumfile = "numberValidation/Fantasy5Picked.txt"
    drawnnumberfile = "fantasy5.txt"
    validatePickedNumbers(callbackFunct, pickednumfile=pickednumfile, pastNumbers=pastNumbers)


'''
    Validate the picked numbers
'''
def validatePickedNumbers(callbackFunct, pickednumfile=None, pastNumbers=None):

    pickedNumbers = None
    pickednumberlistset = None  # = list[(set,numAsString)]

    def parseNumLine(numSeq):
        if numSeq is None or len(numSeq) == 0:
            return None, None

        #debug (numSeq)

        numbers, mega = (None, None)

        numAndMega = numSeq.split(";")
        if len(numAndMega) == 2:
            numbers, mega = numAndMega
        else:
            numbers = numAndMega[0]

        return list(map(lambda s: s.strip(),numbers.split())), mega.strip() if mega is not None else None



    with open(pickednumfile, "rt") as inputF:
        pickedNumbers = list(map(lambda s: parseNumLine(s.strip()),
                                 filter(lambda ss: not ss.startswith("#"),
                                 inputF.readlines()
                                 )
                                 ))

    #debug (pickedNumbers)


    callbackFunct(pastNumbers, pickednumberlistTuple=pickedNumbers)

def validateNumber(pastNumbers, pickednumberlistTuple=None, pickedmegalist=None):
    pastNumbers.validatePickedNumber(pickednumberlistTuple=pickednumberlistTuple, numberofpastnumdrawn=1, numberofpastmegadrawn=5)


def debug(msg):
    print (msg)


def processNumber(pastNumberObject):
    #pastNumberObject.drawNumbers()
    pastNumberObject.genNumber()


def superLotto():
    pastNumber = None
    pastNumbers = genSuperLotto(processNumber, numTickets=5, depth=150, startFrom=3, depthForMega=45)
    validateSuperLottoNumber(validateNumber, pastNumbers)

def execfantasy5():
    pastNumbers = fantasy5(processNumber, numTickets=3, startFrom=0,
             regExp=r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3,5})\s([\d]{10})', depth=20)

    validateFantasy5Number(validateNumber,pastNumbers)


def megaMillion():
    pastNumbers = genMegaMil(processNumber, numTickets=5, depth=41, depthForMega=50)
    validateMegaMillionNumber(validateNumber, pastNumbers)

def powerball():
    pastNumber = genPowerBall(processNumber, numTickets=8,depth=75, depthForMega=50)
    validatePowerballNumber(validateNumber, pastNumber)


MEGA_MILLION = 'megamillion'
POWERBALL = 'powerball'
SUPER_LOTTO = 'superlotto'
FANTASY5 = 'fantasy5'


commandBox = {
    MEGA_MILLION : megaMillion,
    POWERBALL : powerball,
    SUPER_LOTTO : superLotto,
    FANTASY5 : execfantasy5

}

def execute(operationProviderFunc):
    for oper in operationProviderFunc():
        commandBox[oper]()


if __name__ == '__main__':




    def operProvider():
        return \
            [lotteryType]
            #[SUPER_LOTTO]
            #[SUPER_LOTTO, FANTASY5, POWERBALL]
            ##[FANTASY5,MEGA_MILLION]
            ##[MEGA_MILLION]


    lotteryType = sys.argv[1]


    execute(operProvider)