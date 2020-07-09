import os
import os.path as path
import shutil


MONTHS_MAP = {
    "Jan": "01",
    "Feb" : "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "Aug": "08",
    "Sept": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",

}

def renameTaxFile():




    baseFileName = "MedicalInsurance_PremiumDeduction_"
    baseDir = "/Users/michelvu/MichelVu-Taxes/Paystubs/HongNguyen"
    newDir = "/Users/michelvu/MichelVu-Taxes/Paystubs/HongNguyen/RenameForTax"
    newBaseFileName = "Hong_Nguyen_Paystubs_"

    fileList = [file for file in os.listdir(baseDir) if file.find(baseFileName) > -1]

    def newFileName(fileName):
        newFile = fileName
        for index in range(20):

            stringToReplace = str(index) +"_"+baseFileName

            if fileName.find(stringToReplace) == 0:
                newFile = fileName.replace(stringToReplace, "")
                break
            elif fileName.find(baseFileName) == 0:
                newFile = fileName.replace(baseFileName, "")
                break

        return newFile

    #newFileNameList = list(map(lambda f: newFileName(f), fileList))

    def makeDateTimeStamp(fileName):
        def assembleDt(dt):
            retDt = dt
            for key,value in MONTHS_MAP.items():
                if dt.find(key) == 0:
                    retDt = value+"-"+dt.replace(key,"")
                    break
            return retDt

        fromdt, todt, year = fileName.split("_")
        year, fileType = year.split(".")
        return assembleDt(fromdt)+"_to_"+assembleDt(todt)+"_2017"+"."+fileType


    #newFileNameList = list(map(lambda s: (s, newBaseFileName+(makeDateTimeStamp(s))), newFileNameList))



    for fName in fileList:
        newFName = newFileName(fName)
        newFName = newBaseFileName+makeDateTimeStamp(newFName)
        srcFName = path.join(baseDir, fName)
        targetFName = path.join(newDir, newFName)
        shutil.copy(srcFName, targetFName)





renameTaxFile()

