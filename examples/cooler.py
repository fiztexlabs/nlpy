import os
import sys
sys.path.insert(0, os.path.abspath('.'))
from itertools import count

from nlpy import Model
from nlpy.elements import CH
from nlpy.elements import HCS
from nlpy.elements import LR
from nlpy.elements import BVOL_T
from nlpy.elements import SMASS_T
from nlpy.elements import BHEAT
from nlpy.elements import BLJUN
from nlpy.materials import Steel08H18N10T
from nlpy import Event

import numpy as np

class COOLER(Model):
    ids = count(1)
    def __init__(self):
        Model.__init__(self, name="COOLER", id=next(self.ids))

        self.P0_1k = 15.7e6
        self.T0_1k = 40+273.15
        
        self.P0_3k = 0.3e6
        self.T0_3k = 40+273.15

        self.ch1 = CH(
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

        self.ch2 = CH(
            N = 5,
            S = round(np.pi*0.0325**2,7),
            PR = np.pi*2.0*0.0325,
            DZ = 0.488,
            DH = -0.488,
            P = self.P0_1k,
            T = [self.T0_1k, 618.98],
            VOID = 0.,
            TYPE = 0,
            ROU = 0.
        )

        self.ch3 = CH(
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

        self.hcs1 = HCS(
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

        self.hcs2 = HCS(
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
            P = self.P0_1k,
            T = [self.T0_1k, 618.98],
            VOID = 0.
        )

        self.bv2 = BVOL_T(
            P = self.P0_3k,
            T = [self.T0_3k, 618.98],
            VOID = 0.
        )
        
        self.sm1 = SMASS_T(
            GIN = [0., 0.],
            GMOUT = 0.,
            EHIN = [430849.48, 2591220.72]
        )
        
        self.sm2 = SMASS_T(
            GIN = [0., 0.],
            GMOUT = 0.,
            EHIN = [168154.86, 2591220.72]
        )
        

        self.bh_air = BHEAT(
            TYPE = 3,
            BCOND = [1., 293.]
        )
        
        self.bljun = BLJUN(
            TYPE = 0
        )
        
        self.boundaries = [
            self.bh_air, 
            self.bv1, 
            self.bv2,
            self.sm1,
            self.sm2,
            self.bljun
        ]

        self.t_1k_in = Model.Sensor(
            "t_1k_in",
            "T.CH1(1,29);"
        )
        self.t_1k_out = Model.Sensor(
            "t_1k_out",
            "T.CH2(1,2);"
        )
        self.t_3k_in = Model.Sensor(
            "t_3k_in",
            "T.CH3(1,1);"
        )
        self.t_3k_out = Model.Sensor(
            "t_3k_out",
            "T.CH3(1,27);"
        )

        self.action = Event(
            "Action",
            0,
            1,
            [self],
            [
                "IF TAU>2. THEN",
                "T.BVOL_T1(1) = MIN(T.BVOL_T1(1)+DT*30,325.+_t0C);",
                "T.BVOL_T1(2) = WS1P1(2,'P',P.BVOL_T1,2);",
                "GMOUT.SMASS_T1 = MIN(GMOUT.SMASS_T1+DT*0.3,3.056);",
                "GMOUT.SMASS_T2 = MIN(GMOUT.SMASS_T2+DT*1.3889,13.889);",
                "ENDIF"
            ]
        )

        self.rebuild(
            elements = [
                self.ch1, 
                self.ch2,
                self.ch3,
                self.hcs1,
                self.hcs2,
                self.lr_in_mtr, 
                self.lr_out_mtr, 
                self.lr_in_vntr, 
                self.lr_out_vntr,
            ] + self.lr_tr_out + self.boundaries,
            model_layout = [
                "CH1/i - BLJUN1;",
				"CH2/i - BLJUN1;",
				"CH3/o - BLJUN1;",
				"CH1(29) - LR1;",
				"CH1(7:25) - LR(5:23);",
				"CH2/o - CH1(1);",
				"CH2(5) - LR2;",
				"CH3(4) - LR4;",
				"CH3(28) - LR3;",
				"HCS1(1:20)/1 - CH3(6:25);",
				"HCS1(1:20)/2 - CH1(6:25);",
				"HCS2(1:26)/1 - CH1(1:26);",
            ],
            boundary_layout = [
				"CH1/o - BVOL_T1;",
				"CH2(1) - SMASS_T1;",
				"CH3/i - BVOL_T2;",
				"CH3(28) - SMASS_T2;",
				"HCS2(1:26)/2 - BHEAT1;"
            ],
            sensors=[self.t_1k_in,self.t_1k_out,self.t_3k_in,self.t_3k_out],
            submodels = [],
            submodel_links_layout = [],
            events = [self.action]
        )


cool = COOLER()