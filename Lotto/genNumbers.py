__author__ = 'michelvu'

import os
import re, random
from random import randrange

class LottoNumbers:
    def __init__(self):
        self.pastNumbers = []
        self.mega = []
        self.numTickets = 1
        self.depthDraw = 25
        self.startFrom = 3
        self.depthDrawForMega = 9;

    def setNumTicket(self, numtickets):
        self.numTickets = numtickets

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

        self.mega.append(megaNumber)


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


    def genNumber(self):
        repeatedNumbers = set()

        selNumberSet = self.pastNumbers[self.startFrom:self.depthDraw]

        #--- Find the repeated number in setNummberSet ----
        

        for numberSet in selNumberSet:
            for numberSetinPast in selNumberSet:
                matchNumberSet = numberSet.intersection(numberSetinPast)
                if matchNumberSet == numberSet:
                    continue
                else:
                     repeatedNumbers.update(matchNumberSet)

        if(len(repeatedNumbers)):

            #print (repeatedNumbers)
            self.printListNumber(repeatedNumbers)

            selectedTicket = self.drawTicket(poolNumberSet=repeatedNumbers)



            if len(self.mega):
                self.drawMega()

    def printListNumber(self, numberList):

        inList = list(numberList)
        plist = inList[0:20];

        print (plist)
        pList = inList[21:]
        print (plist)


    def shuffleBucket(self, bucketNumbers):
        useBucket = bucketNumbers
        for x in range(randrange(1, 10)):
            random.shuffle(useBucket)

        return useBucket;

    def drawTicket(self, poolNumberSet=set()):
        numberInPool = len(poolNumberSet)
        elibibleNumbers = list(poolNumberSet)
        try:
            pass
        except Exception as e:
            print (e)

        ticket = set()
        lastDrawnNumbers = self.pastNumbers[0]
        print (">>>Last drawn number: ", lastDrawnNumbers)
        for x in range(self.numTickets):
            while(True):

                elibibleNumbers = self.shuffleBucket(elibibleNumbers)
                pickedNumber = random.sample(elibibleNumbers,1)[0]
                if pickedNumber in lastDrawnNumbers:
                    continue

                if isNumberInsetInsideOfRange(numberset=ticket, numRange=5, checknumber=pickedNumber):
                    continue

                ticket.add(pickedNumber)
                if(len(ticket) >= 5):
                    break
            #numbersForTicket = random.sample(elibibleNumbers, 5)
            print (ticket)
            ticket.clear()



    def drawMega(self):
        numberInPool = len(self.mega)
        megaPool = self.mega[:self.depthDrawForMega]

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
        print ("Repeated mega:",repeatedMegaNumber)
        for x in range(self.numTickets):
            numbersForTicket = random.sample(repeatedMegaNumber, 1)
            print (numbersForTicket)

def isNumberInsetInsideOfRange(numberset=None, numRange=None, checknumber=None):
    if numberset is None or numRange is None or checknumber is None:
        return False
    if not len(numberset):
        return True
    invalid = False
    for x in numberset:
        testx = int(x)
        pickedNumber = int(checknumber)
        invalid = testx > (pickedNumber - numRange) and testx < (pickedNumber + numRange)
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


def genPowerBall(callbackFunct, regExp=None, numTickets=2, depth=33, startFrom=2, depthForMega=10):
    baseDir = "/Users/michelvu/Python/Learning/Lotto/data/"
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_powerball.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    callbackFunct(pastNumbers)

def genMegaMil(callbackFunct, regExp=None, numTickets=5, depth=25, startFrom=2,depthForMega=10):
    baseDir = "/Users/michelvu/Python/Learning/Lotto/data/"
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_megamillion.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    callbackFunct(pastNumbers)


def genSuperLotto(callbackFunct, regExp=None, numTickets=5, depth=25, startFrom=2,depthForMega=10):
    baseDir = "/Users/michelvu/Python/Learning/Lotto/data/"
    pastNumbers = getNumber("{}{}".format(baseDir, "numbers_superlotto.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDrawForMega = depthForMega
    callbackFunct(pastNumbers)


def fantasy5(callbackFunct, regExp=None, numTickets=4, depth=50, startFrom=2, depthForMega=10):
    baseDir = "/Users/michelvu/Python/Learning/Lotto/data/"
    pastNumbers = getNumber("{}{}".format(baseDir, "fantasy5.txt"), regExp)
    pastNumbers.numTickets = numTickets
    pastNumbers.startFrom = startFrom
    pastNumbers.depthDraw = depth
    pastNumbers.depthDrawForMega = depthForMega
    callbackFunct(pastNumbers)

def processNumber(pastNumberObject):
    #pastNumberObject.drawNumbers()
    pastNumberObject.genNumber()

r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3,5})\s([\d]{10})\s([\d]{1,2})'
if __name__ == '__main__':
    genPowerBall(processNumber, numTickets=4,depth=25, depthForMega=25)
    #genMegaMil(processNumber, numTickets=10, depth=25, depthForMega=20)
    #fantasy5(processNumber, numTickets=4, startFrom=2, regExp=r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3,5})\s([\d]{10})', depth=28)
    #genSuperLotto(processNumber,numTickets=5, depth=25, startFrom=3, depthForMega=25)
