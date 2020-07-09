import pandas as pd
import numpy as np
from functools import reduce
from datetime import datetime


class DataFileLoader:
    def __init__(self, dataFile):
        self.dataFile = dataFile
        self.dataFrame = None

    def matchMega(self, date=None, inMega=None):
        if date is None or inMega is None:
            return False;

        return self.dataFrame[self.dataFrame[5] == inMega]

    def makeNumberEntry(self, numberSet, mega=None):

        draw = sorted(list(map(lambda n: str(n) if n > 9 else "0" + str(n), numberSet)))

        if mega:
            draw.append(str(mega) if mega > 9 else "0" + str(mega))

        return pd.Series(draw)

    def matchNumberForDate(self, dateAsString=None, number_to_match=None, mega=None):
        if dateAsString is None or number_to_match is None:
            return False

        if not self.getDataFrame().index.contains(pd.Timestamp(dateAsString)):
            return "Draw for date " + dateAsString + " not available in the data frame"

        draw = self.dataFrame.loc[dateAsString]

        # print ("draw:", draw)

        result = None

        if not len(draw):
            return None

        entry = self.makeNumberEntry(number_to_match, mega)

        # print (">>>Entry", entry)

        if not len(entry):
            return "Draw for date " + dateAsString + " not available in the data frame"

        # --- All number match
        if entry.equals(draw):
            return "Match all numbers!!!"

        # ---- partial matches ---
        matchMega = False
        drawSet = draw[0:5]
        entrySet = entry[0:5]

        drawMega = draw[5:6]
        entryMega = entry[5:6]



        matchNumberSet = set(drawSet.to_dict().values()).intersection(set(entry.to_dict().values()))

        if len(drawMega) and len(entryMega):
            matchMega = drawMega.equals(entryMega)

        # print (matchNumberSet)
        # print (">>>>", matchMega)

        result = "Mached Number[%s]: %s *** Mached Mega: %s  *** Drawn number: %s" % (len(matchNumberSet),
        " ".join(matchNumberSet), str(matchMega), " ".join(drawSet))

        return result

    def exist(self, number, ret_result=False):
        number.sort()
        cond = []
        i = 0
        for n in number:
            cond.append(self.dataFrame[i] == n)
            i += 1

        allCond = reduce(lambda x, y: x & y, cond)

        if ret_result:
            res = self.dataFrame[allCond]
            return res, len(res) > 0
        else:
            return len(self.dataFrame[allCond]) > 0

    def read(self):

        def toDateTime(dateString):
            month, date, year = map(lambda x: x.strip(" ,"), dateString.split())
            dtime = datetime.strptime(month + (date if len(date) == 2 else "0" + date) + year, "%b%d%Y")
            return dtime

        def extractNumberAndMega(numberIn):
            mega = None
            number = None
            numSep =  numberIn.count('\t')
            if numSep == 2:
                _, number, mega, *rest = map(lambda x: x, numberIn.split('\t'))
            elif numSep == 1:
                _, number, *rest = map(lambda x: x, numberIn.split('\t'))
            else:
                number, *rest = map(lambda x: x, numberIn.split())

            number = [number[x: x + 2:] for x in [0, 2, 4, 6, 8]]
            number.sort()
            if mega:
                megaS = mega.rstrip()
                mega = "0" + megaS if len(megaS) < 2 else megaS
                number.append(mega)
            return number

        with open(self.dataFile, mode="r") as inputF:

            data = {}
            lines = map(lambda l: l.strip(), inputF.readlines())
            for ln in lines:
                date, numbers = [x for x in map(lambda x: x.strip(), ln.split("-"))]

                data[toDateTime(date)] = extractNumberAndMega(numbers)
        self.dataFrame = pd.DataFrame(data)
        self.dataFrame = self.dataFrame.transpose()

    def getDataFrame(self):

        return self.dataFrame

