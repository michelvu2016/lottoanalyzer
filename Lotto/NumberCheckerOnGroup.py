

class NumberCheckerOnGroup:

    @classmethod
    def numberToGroup(cls, tNumber):
        clsNumber = 1
        if tNumber >= 1 and tNumber <= 9:
            clsNumber = 1
        elif tNumber >= 10 and tNumber <= 19:
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

        return clsNumber

    def __init__(self):
        self.numberGroup = None

    def setGroup(self, numberGroupTuple):
        self.numberGroup = list(numberGroupTuple)

    def matchGroup(self, numberList):

        groupList = list(map(lambda n: NumberCheckerOnGroup.numberToGroup(n), numberList))

        return groupList == self.numberGroup


if __name__ == '__main__':
    numberCheckerOnGroup = NumberCheckerOnGroup()
    numberCheckerOnGroup.setGroup((1,20,30,40,40))
    numList = list([3,25,34,45,41])
    numberCheckerOnGroup.matchGroup(numList)
    NumberCheckerOnGroup.numberToGroup(20)
