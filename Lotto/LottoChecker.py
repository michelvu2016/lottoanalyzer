
import pandas as pd
from lotomachine.lottomachine import DataFileLoader

from collections import defaultdict



class TicketLoader:

    BASE_DIR = "/Users/michelvu/Python/Learning/Lotto/tickets/"

    def __init__(self, ticketFile):
        self.entries = []
        self._loadFile(TicketLoader.BASE_DIR+ticketFile)

    def _processNumberEntry(self, numberEntry):
        numberS = numberEntry.split(",")
        mega = None
        if "-" in numberEntry: #Process embedded mega
            num, mega = map(lambda n: n.strip(), numberS.pop().split("-"))
            numberS.append(num)

        return list(map(lambda n: int(n), numberS)), int(mega) if mega else None


    def _loadFile(self, filePath):
        with open (filePath) as infile:
            lines = map(lambda s: s.strip(), infile.readlines())
            date = False
            number = True

            entry = {
                'drawDate' : '',
                'numberList' : []
            }

            numberS = {
                'number':[],
                'mega': None
            }

            for line in lines:

                if not line:
                    continue

                if "Date:" in line:
                    date = True
                    number = False
                    if entry['numberList']:
                        self.entries.append(entry)

                    entry = {
                        'drawDate': None,
                        'numberList': []
                    }

                    continue
                elif "Numbers:" in line:
                    number = True
                    date = False
                    numberS = {
                        'number':None,
                        'mega': None
                        }
                    #Init structure
                    continue
                elif date:
                    entry['drawDate'] = line
                elif number:
                    numberLine = self._processNumberEntry(line)
                    numberS['number'] = numberLine[0]
                    numberS['mega'] = numberLine[1]
                    entry['numberList'].append(numberS)
                    numberS = {
                        'number': None,
                        'mega': None
                    }

            if entry['numberList']:
                self.entries.append(entry)

    def process(self, processorFunc):
        for entry in self.entries:
            processorFunc(entry)

class CheckNumber:
    def __init__(self, dataFile):
        self.dataLoader = DataFileLoader(dataFile)
        self.dataLoader.read()

    def isTicketExpired(self, ticketDateAsString):
        return (pd.datetime.now() - pd.to_datetime(ticketDateAsString)).days > 180

    def validate(self, dateAsString, numberList, mega=None):

        if self.isTicketExpired(dateAsString):
            print ("***** Ticket expired (over 180 days ******")

        result = self.dataLoader.matchNumberForDate(dateAsString, numberList, mega)
        print('%s %s %s %s ' % (dateAsString, numberList, mega if mega else "", result))


    def getDataFrame(self):
        return self.dataLoader.getDataFrame()

DATA_FILE_DRAWN_NUMBERS_BASE_DIR = "/Users/michelvu/Python/Learning/Lotto/data/"

def getFullDrawnDataFile(dataFileName):
    return DATA_FILE_DRAWN_NUMBERS_BASE_DIR+dataFileName





'''
  Input structur:
  [{
      drawnDate : '2018-04-12',
      numberList: [{
                    number: [12,34,5,7,8],
                    mega : Optional
                   }]


  }]

'''
def genericChecker(numbersToCheck, dataFile):

    checkNumber = CheckNumber(getFullDrawnDataFile(dataFile))




    def checkTicketEntry(ticket):
        drawDate, numList = ticket['drawDate'], ticket['numberList']



        print(drawDate, numList)
        for numSel in numList:
            #print("numSel", numSel)
            numberList, mega = numSel['number'], numSel['mega']
            #print(numberList, mega)
            if type(numList) == list and type(mega) == list:
                for index in range(len(numList)):
                    checkNumber.validate(drawDate, numberList[index], mega[index])
            else:

                checkNumber.validate(drawDate, numberList, mega)

    if type(numbersToCheck) == list:
        for ticket in numbersToCheck:
            checkTicketEntry(ticket)
    else:
            checkTicketEntry(numbersToCheck)



def numberwithMegaChecker(numbersToCheck, dataFileIn=None):
    print ("========= Validate number for SuperLotto **************")
    genericChecker(numbersToCheck, dataFile=dataFileIn)


def fantasy5Checker(numbersToCheck, dataFileIn=None):
    print ("========= Validate number for Fantasy 5 **************")
    genericChecker(numbersToCheck, dataFile=dataFileIn)



def validateFantasy5TicketFile(ticket):

    ticketLoader = TicketLoader(ticketFile='fantasy5.txt')

    ticketLoader.process(lambda e:
                         fantasy5Checker(e, dataFileIn="fantasy5.txt")
                         #print (e)
                         )

def validateSuperlottoTicketFile():

    ticketLoader = TicketLoader(ticketFile='superlotto.txt')

    ticketLoader.process(lambda e:
                         numberwithMegaChecker(e, dataFileIn="numbers_superlotto.txt")
                         #print (e)
                         )

def validatelottoTicketFile(ticketFileIn=None, hasMega=None, dataFileInput=None):

    ticketLoader = TicketLoader(ticketFile=ticketFileIn)

    ticketLoader.process(lambda e:
                         numberwithMegaChecker(e, dataFileIn=dataFileInput)
                            if hasMega else fantasy5Checker(e, dataFileIn=dataFileInput)
                         #print (e)
                         )

def validatelottoTicketFileWithExposedDataFrame(dataFileInput=None, dataFrameProcessor=None):

    checkNumber = CheckNumber(getFullDrawnDataFile(dataFileInput))

    if dataFrameProcessor is not None:
        dataFrameProcessor(checkNumber.getDataFrame())



if __name__ == '__main__':

    def runNumberValidation():
        print ("------ Runing checker ------")

        print ("Pandas version:", pd.__version__)




    def debug():
        dataFile = ["fantasy5.txt","numbers_superlotto.txt"][1]
        dataLoader = DataFileLoader(getFullDrawnDataFile(dataFile))
        dataLoader.read()

        df = dataLoader.getDataFrame()
        print (df.loc['2018-05-19'])

    def test1():

        ticketLoader = TicketLoader(ticketFile='fantasy5.txt')

        ticketLoader.process(lambda e:
                             fantasy5Checker(e)
                             #print (e)
                             )


    #runNumberValidation()

    #debug()

    #validateFantasy5TicketFile()

    #validateSuperlottoTicketFile()


    ticketTypeMap = {
            "fantasy5" : {
                'ticketFileIn' : "fantasy5.txt",
                'dataFileInput' : "fantasy5.txt",
                'hasMega' : False
            },
        "superlotto": {
            'ticketFileIn': "superlotto.txt",
            'dataFileInput': "numbers_superlotto.txt",
            'hasMega': True
        },
        "powerball": {
            'ticketFileIn': "powerball.txt",
            'dataFileInput': "numbers_powerball.txt",
            'hasMega': True
        },
        "megamillion": {
            'ticketFileIn': "numbers_megamillion.txt",
            'dataFileInput': "megamillion.txt",
            'hasMega': True
        },
    }

    COMMAND_SELECTOR = {'NUM_CHECK': 100, 'NUMBER_VALIDATOR' : 200}

    command = COMMAND_SELECTOR[
                            'NUM_CHECK'

                        ]


    TICKET_NAME = "superlotto" #"superlotto", "powerball","megamillion","fantasy5"


    print(ticketTypeMap[TICKET_NAME]['ticketFileIn'])


    if command == 100:
        validatelottoTicketFile(ticketFileIn=ticketTypeMap[TICKET_NAME]['ticketFileIn'],
                                dataFileInput=ticketTypeMap[TICKET_NAME]['dataFileInput'],
                                hasMega=ticketTypeMap[TICKET_NAME]['hasMega'])
    elif command == 200:

        outputFile = '/Users/michelvu/Python/Learning/Lotto/data/capturedDF.csv'
        def processDataFrame(dataFrame):
            dataFrame.to_csv(outputFile)


        validatelottoTicketFileWithExposedDataFrame(dataFileInput=ticketTypeMap[TICKET_NAME]['dataFileInput'],
                                dataFrameProcessor=processDataFrame)