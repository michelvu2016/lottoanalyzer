import csv

def writeCsv(data=[]) :
    csvFile = "C:/development/testData/test.csv"
    with open(csvFile, 'w', newline='') as csvFileObj:
        writer = csv.writer(csvFileObj, delimiter=",")
        writer.writerows(data)


def dictValToArray(d={}) :
    writeCsv([v for v in d.values()])
    


def testTuple():
    myTuple = (2,4,5)

    print (myTuple[1])


    mySet = set(('23', '12', '09','12'))
    matchSet = '23' in mySet

    print (matchSet)

#testTuple()

#print (18+18+24)

#writeCsv(['clena','tony', 'hong', 'mom', 'angels'])

dictValToArray({'a': ['me','mon','ma'], 'b': ['dad', 'broth']})