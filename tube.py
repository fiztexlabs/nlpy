from nlpy.model import Model
from itertools import count
from nlpy.elements import CH
from nlpy.elements import HCS
from nlpy.elements import BVOL_T
from nlpy.elements import BHEAT
from nlpy.materials import Steel08H18N10T

import numpy as np

class Tube(Model):
    ids = count(1)
    def __init__(self):
        Model.__init__(self, name="Tube", id=next(self.ids))

        self.ch1 = CH(
            N = 5,
            S = 0.000120763,
            PR = 
            np.array([
                0.000120763,
                0.000120763,
                0.000120763,
                0.000120763,
                0.0120763
            ]),
            DZ = 2.490,
            DH = 2.490,
            P = 1.e6,
            T = [293.0, 453.15],
            VOID = 0.,
            TYPE = 0,
            ROU = 2.e-5)

        self.hcs1 = HCS(
            N = 5,
            KL = 1,
            K = 5,
            TYPE = 0,
            COOR = 1,
            XL = np.array([
                6.2e-3,
                8.0e-3
            ]),
            X = np.linspace(6.2e-3,8.0e-3,5),
            MAT = [Steel08H18N10T],
            DFZ = 0.30575,
            B = 36.01482461,
            NGE = 0,
            KIND = np.array([6,4])
        )

        self.bv1 = BVOL_T(
            P = 1.e6,
            T = [293.0, 453.15],
            VOID = 0.
        )

        self.bv2 = BVOL_T(
            P = 1.e6,
            T = [293.0, 453.15],
            VOID = 0.
        )

        self.bh = BHEAT(
            TYPE = 3,
            BCOND = [1., 293.]
        )

        self.t_in = Model.Sensor(
            "t input",
            "T.CH1(1,1);"
        )
        self.p_in = Model.Sensor(
            "p input",
            "P.CH1(1);"
        )

        self.rebuild(
            elements = [self.ch1, self.hcs1, self.bh, self.bv1, self.bv2],
            model_layout = [
                "CH1(1:5) - HCS1(1:5)/1;",
                "HCS1(1:5)/2 - BHEAT1;"
            ],
            boundary_layout = [
                "CH1/i - BVOL_T1;",
                "CH1/o - BVOL_T2;"
            ],
            sensors=[self.t_in,self.p_in],
            submodels = [],
            submodel_links_layout = []
        )


# tube_model1 = Tube()
# from nlpy import write_data
# write_data(tube_model1.__diarnostics__,"./diag1.txt")
# tube_model2 = Tube()
# write_data(tube_model2.__diarnostics__,"./diag2.txt")

print('a')