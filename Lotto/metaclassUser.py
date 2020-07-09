
from metatester import Base

class Derived(Base):
    def bar(self):
        return 'bar'




d = Derived()

print(d.foo())