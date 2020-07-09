__author__ = 'michelvu'


class Pick_8_9_10:
    def draw(self):
        return [(12,34,56,67,34),(15,64,57,47,64),(22,54,76,17,24)]



class Pick_last3:
    def draw(self):
        return [(22,44,66,87,34),(55,24,47,67,24),(12,34,56,27,24)]


def toString(t):
     r = map(lambda x: "0"+str(x) if x < 10 else str(x), t)
     return " ".join(r)


eigthNineTen =  Pick_8_9_10().draw()

print (eigthNineTen)

eigthNineTen =  Pick_last3().draw()

print (eigthNineTen)

sample = [(12,34,56,67,4),(15,64,57,7,64),(22,54,76,17,24)]

r = tuple(",".join((map(toString, sample))))

print (r)


