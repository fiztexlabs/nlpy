from nlpy.model import Model
from itertools import count
from tube import Tube


class TJUN(Model):
    ids = count(1)
    def __init__(self):
        Model.__init__(self, name="TJUN", id=next(self.ids))
        self.pipe1 = Tube()
        self.pipe2 = Tube()
        self.pipe2.bv2.disable()

        self.rebuild(
            [],
            [],
            [
                "CH{1}/o - CH{2}(2);",
            ],
            [],
            [self.pipe1,self.pipe2]
        )

tjun = TJUN()

print("tjun")