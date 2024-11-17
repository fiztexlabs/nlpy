import numpy as np

from nlpy import Task
# from tube import tube_model1, tube_model2

from tjun import tjun
# from cooler import cool

# tube_model1.bv1.disable()

test = Task(
    'test', 
    [tjun],
    restart = 0,
    title = "\'vb.036.003\'",
    dt_max = 0.01,
    dt_out = 1.,
    fin_tim = 600.,
    dt_sav = 1.,
    append_res = 1,
    append_sav = 1,
    check_only = 0,
    local_err = 1.0e-4,
    ngas = "\'H2O, N2, H2, HE, O2\'",
    dt_diag = 1.,
    inf = 1,
    accel_stat = 0,
    okbm = 1,
    # nwsp_dat = "\'n:\\Dep49\\Common\\MCD\\Utils\\KORSAR-KUPOL\\nwsp_dat\'"
    nwsp_dat = "\'c:\\codes\\KORSAR\\nwsp_dat\'",
    # nwsp_dat = "\'d:\\KORSAR\\nwsp_dat\'",
    _monPer = 2.,
    _diag = 2.
)

test.write_kordat("./kortest/kordat")

