

class BaseMeta(type):
    def __new__(cls, name, bases, body):

        if name != 'Base':
            if not 'bar' in body:
                raise TypeError("Bad user class")
        return super().__new__(cls, name, bases, body)









class Base(metaclass=BaseMeta):
    def foo(self):
        return self.bar()

    def __init_subclass__(cls, **kwargs):
        pass




def method1():

    old_bc = __build_class__

    def my_bc(*a, **kw):
        print (a, kw)
        return old_bc(*a, **kw)

    def validateSubClass(func, name, base=None, **kw):
        if base is Base:
            print('Check if bar method defined')

        if base is not None:
            return old_bc(func, name, base, **kw)

        return old_bc(func, name, base, **kw)

    import builtins

    builtins.__build_class__ =  validateSubClass     ##my_bc

