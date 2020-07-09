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


        for numberSet in self.genNumberSample():
            if 17 in numberSet:
                print ("found 17")
            for numberSetinPast in selNumberSet:
                matchNumberSet = numberSet.intersection(numberSetinPast)
                if matchNumberSet == numberSet:
                    continue
                else:

                     repeatedNumbers.update(matchNumberSet)

        if(len(repeatedNumbers)):
            print (repeatedNumbers)
            self.drawTicket(poolNumberSet=repeatedNumbers)
            if len(self.mega):
                self.drawMega()


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
        for x in range(self.numTickets):
            while(True):

                elibibleNumbers = self.shuffleBucket(elibibleNumbers)

                ticket.add(random.sample(elibibleNumbers,1)[0])
                if(len(ticket) >= 5):
                    break
            #numbersForTicket = random.sample(elibibleNumbers, 5)
            print (ticket)
            ticket.clear()



    def drawMega(self):
        numberInPool = len(self.mega)
        megaPool = self.mega[:self.depthDrawForMega]
        for x in range(self.numTickets):
            numbersForTicket = random.sample(megaPool, 1)
            print (numbersForTicket)


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
    genPowerBall(processNumber, numTickets=1,depth=17, depthForMega=20)
    #genMegaMil(processNumber, numTickets=3, depth=12, depthForMega=8)
    #fantasy5(processNumber, regExp=r'^([A-Za-z]{3}\s[\d]{1,2}[\,]\s[\d]{4})\s[\-]\s([\d]{3,5})\s([\d]{10})', depth=10)
    #genSuperLotto(processNumber,numTickets=1, depth=20, startFrom=3, depthForMega=20)
