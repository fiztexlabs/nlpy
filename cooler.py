from itertools import count
from nlpy.model import Model
from nlpy.elements import CH
from nlpy.elements import HCS
from nlpy.elements import LR
from nlpy.elements import BVOL_T
from nlpy.elements import BHEAT
from nlpy.materials import Steel08H18N10T

import numpy as np

class COOLER(Model):
    ids = count(1)
    def __init__(self):
        Model.__init__(self, name="COOLER", id=next(self.ids))

        self.P0_1k = 15.7e6
        self.T0_1k = 40+273.15
        
        self.P0_3k = 0.3e6
        self.T0_3k = 40+273.15

        self.mtr_in = CH(
            N = 29,
            S = np.array([
			    0.027022,
			    0.072534,
			    0.106221,
			    0.125180,
			    0.127486,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.005300,
			    0.196350,
			    0.196350,
			    0.003318,
			    0.003318
            ]),
            PR = np.array([
			    0.582729,
			    0.954718,
			    1.155341,
			    1.254218,
			    3.707079,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.325000,
			    1.570796,
			    1.570796,
			    0.204204,
			    0.204204
            ]),
            DZ = np.array([
			    0.027850,
			    0.032400,
			    0.032400,
			    0.032400,
			    0.432475,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.432475,
			    0.100000,
			    0.125000,
			    0.125000
            ]),
            DH = np.array([
			    0.027850,
			    0.032400,
			    0.032400,
			    0.032400,
			    0.432475,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.432475,
			    0.100000,
			    0.125000,
			    0.125000
            ]),
            P = self.P0_1k,
            T = [self.T0_1k, 618.98],
            VOID = 0.,
            TYPE = 6,
            ROU = 0.
        )

        self.mtr_out = CH(
            N = 5,
            S = np.pi*0.0325**2,
            PR = np.pi*2.0*0.0325,
            DZ = 0.488,
            DH = -0.488,
            P = self.P0_1k,
            T = [self.T0_1k, 618.98],
            VOID = 0.,
            TYPE = 0,
            ROU = 0.
        )

        self.vntr = CH(
            N = 28,
            S = np.array([
			    0.003318,
			    0.003318,
			    0.003318,
			    0.003318,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.004347,
			    0.003318,
			    0.003318
            ]),
            PR = np.array([
			    0.204204,
			    0.204204,
			    0.204204,
			    0.204204,
			    0.233722,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    1.402258,
			    0.204204,
			    0.204204
            ]),
            DZ = np.array([
			    0.572250,
			    0.572250,
			    0.572250,
			    0.572250,
			    0.381000,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.305750,
			    0.298000,
			    0.260000,
			    0.250000
            ]),
            DH = np.array([
			    -0.572250,
			    -0.572250,
			    -0.572250,
			    -0.572250,
			    0.381000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.055000 ,
			    0.298000 ,
			    0.260000 ,
			    0.250000 
            ]),
            P = self.P0_3k,
            T = [self.T0_3k, 406.67],
            VOID = 0.,
            TYPE = 0,
            ROU = 0.
        )

        self.tubes = HCS(
            N = 20,
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

        self.case = HCS(
            N = 26,
            KL = 1,
            K = 5,
            TYPE = 0,
            COOR = 1,
            XL = np.array([
                0.26,
                0.28
            ]),
            X = np.linspace(0.26,0.28,5),
            MAT = [Steel08H18N10T],
            DFZ = np.array([
			    0.125214,
			    0.074405,
			    0.050303,
			    0.039758,
			    0.432475,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.055000,
			    0.432475,
			    0.100000
            ]),
            B = 1.,
            NGE = 10,
            KIND = np.array([0])
        )

        self.lr_in_mtr = LR(
            CSI1 = 3.525,
            CSI2 = 3.525,
        )

        self.lr_out_mtr = LR(
            CSI1 = 2.844,
            CSI2 = 2.844,
        )

        self.lr_in_vntr = LR(
            CSI1 = 2.035,
            CSI2 = 2.035,
        )

        self.lr_out_vntr = LR(
            CSI1 = 2.379,
            CSI2 = 2.379,
        )

        self.lr_tr_out = []
        for i in range(19):
            self.lr_tr_out.append(
                LR(
                    CSI1 = 0.000524,
                    CSI2 = 0.000524
                )
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

        self.bh_air = BHEAT(
            TYPE = 3,
            BCOND = [1., 293.]
        )

        # self.t_in = Model.Sensor(
        #     "t input",
        #     "T.CH1(1,1);"
        # )
        # self.p_in = Model.Sensor(
        #     "p input",
        #     "P.CH1(1);"
        # )

        self.rebuild(
            elements = [
                self.mtr_in, 
                self.mtr_out,
                self.vntr,
                self.tubes,
                self.case,
                self.lr_in_mtr, 
                self.lr_out_mtr, 
                self.lr_in_vntr, 
                self.lr_out_vntr,
            ] + self.lr_tr_out + [
                self.bh_air, 
                self.bv1, 
                self.bv2
            ],
            model_layout = [
                "CH1(1:5) - HCS1(1:5)/1;",
                "HCS1(1:5)/2 - BHEAT1;"
            ],
            boundary_layout = [
                "CH1/i - BVOL_T1;",
                "CH1/o - BVOL_T2;"
            ],
            sensors=[],
            submodels = [],
            submodel_links_layout = []
        )


cool = COOLER()
print('a')