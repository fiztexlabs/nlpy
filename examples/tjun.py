import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from itertools import count

from nlpy import Model
from nlpy import Event
from tube import Tube


class TJUN(Model):
    ids = count(1)
    def __init__(self):
        Model.__init__(self, name="TJUN", id=next(self.ids))
        self.pipe1 = Tube()
        self.pipe2 = Tube()
        self.pipe2.bv2.disable()

        self.rebuild(
            elements = [],
            model_layout = [],
            boundary_layout = [],
            submodel_links_layout = 
            [
                "Tube2.CH1/o - Tube1.CH1(2);",
            ],
            sensors = [],
            submodels = [self.pipe1,self.pipe2],
            events = [
                Event(
                    "_print_dat",
                    0,
                    1,
                    [self,self.pipe1,self.pipe2],
                    [
                        "PRINT \'Tube1 BV \', P.Tube1.BVOL_T1;"
                        "PRINT \'Tube2 BV \', P.Tube2.BVOL_T1;"
                    ]
                )

            ]
        )

tjun = TJUN()

print("tjun")