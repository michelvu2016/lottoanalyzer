import functools as ft
import numpy as np
import pandas as pd

# t = []
# t.append({'53', '65', '70', '15', '23'})
#
# t.append({'61', '24', '46', '70', '04'})
#
# t.append({'66', '30', '40', '43', '23'})

ta = ['01', '02', '03', '04', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '52', '53', '54', '56', '57', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70']


def toUniqueSet(arrayOfSet):

    def updateSet(cumulaterSet, dataSet):
        cumulaterSet.update(dataSet)
        return cumulaterSet

    s = ft.reduce(lambda cs, ds: updateSet(cs, ds),arrayOfSet, set())

    s = sorted(s)


    return s


def toMultiDimArray(inArray):
    ar = np.array(inArray)

    return ar


def listWrapper(inList, numberElmEachLine, processFunc):

    startX = 0

    done = False
    while not done:
        endX = startX + numberElmEachLine if numberElmEachLine <= len(inList) else len(inList)


        r = inList[startX:endX]

        processFunc(r)

        startX = endX
        done = startX >= len(inList)


def numStr(num, numOfDigits):
    return str(num) if num >= 10 else "0"+str(num)


def gapNumbersInSet(inSet):
    retSet = set()
    startNum = 1
    lastNum = int(inSet[-1])

    while startNum <= lastNum:
        numAsStr = numStr(startNum,2)
        if numAsStr not in inSet:
            retSet.add(numAsStr)

        startNum += 1

    return retSet






