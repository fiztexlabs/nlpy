import numpy as np
from typing import List
import os
import copy

from . import Model

class Task:
    """
    Зона задания в РК КОРСАР
    =====

    Attributes
    ----------
    task_name : str
        Название задачи
        
    models : List[model]
        Список моделей в задаче

    kordat : List[str]
        Массив строк, содержащих зону задания kordat

    Methods
    ----------
    rebuild
        Перестраивает зону задания kordat

    write_kordat
        Записывает kordat в файл
    """
    def __init__(
            self,
            task_name: str,
            models: List[Model],
            **kwargs: dict
        ):
        self.task_name = task_name

        self.models = models

        self.kordat = []

        self.task_keys = kwargs

        self.rebuild()

    def rebuild(self):
        """
        Перестроить kordat
        """
        self.__task_keys__ = [
            "!!bb Task keys",
            '\trestart = '+str(self.task_keys['restart'])+";",
            '\ttitle = '+str(self.task_keys['title'])+";",
            '\tdt_max = '+str(self.task_keys['dt_max'])+";",
            '\tdt_out = '+str(self.task_keys['dt_out'])+";",
            '\tfin_tim = '+str(self.task_keys['fin_tim'])+";",
            '\tdt_sav = '+str(self.task_keys['dt_sav'])+";",
            '\tappend_res = '+str(self.task_keys['append_res'])+";",
            '\tappend_sav = '+str(self.task_keys['append_sav'])+";",
            '\tcheck_only = '+str(self.task_keys['check_only'])+";",
            '\tlocal_err = '+str(self.task_keys['local_err'])+";",
            '\tngas = '+str(self.task_keys['ngas'])+";",
            '\tdt_diag = '+str(self.task_keys['dt_diag'])+";",
            '\tinf = '+str(self.task_keys['inf'])+";",
            '\taccel_stat = '+str(self.task_keys['accel_stat'])+";",
            '\tokbm = '+str(self.task_keys['okbm'])+";",
            '\tnwsp_dat = '+str(self.task_keys['nwsp_dat'])+";",
            '\t_monPer = '+str(self.task_keys['_monPer'])+";",
            '\t_diag = '+str(self.task_keys['_diag'])+";",
            "!!eb Task keys"
        ]
        self.__globals__ = []
        self.__outs__ = [
            "!!bb OUTs",
            "\tOUT _Out;",
            "!!eb OUTs"
        ]
        self.__layout__ = []
        self.__calls__ = []
        self.__sets__ = []
        self.__main__ = []
        self.__sensors__ = []
        
        self.__data__ = []
        self.__dignostics__ = []
        self.__monitors__ = []
        self.__events__ = ["!!bb EVENTs"]
        self.__outputs__ = [
            "WRITE",
            "\tDT",
            "\t,dt_out",
            "\t,dt_max",
            # "\t,dt_diag",
            # "\t,_monPer",
            "\t,dt_sav",
            "\t,restart"
            # "\t,_tauRest"
        ]

        # find same materials
        mats = []
        for m in self.models:
            m.rebuild(
                elements=copy.copy(m.all_elements), 
                model_layout=copy.copy(m.model_layout), 
                boundary_layout=copy.copy(m.boundary_layout), 
                sensors=copy.copy(m.sensors), 
                submodels=copy.copy(m.submodels),
                submodel_links_layout=copy.copy(m.submodel_links_layout),
                events=copy.copy(m.events)
            )
            for el in m.elements_submodels:
                if el.is_enabled():
                    if el.el_type() == "HCS":
                        mats.extend(el.MAT)
        task_materials = list(set(mats))

        for mat in task_materials:
            self.__globals__.extend(mat.__globals__)


        self.__monitors__ = [
            "EVENT _Monitors",
            "\ttype = ALW;",
            "\treplace = 1;",
            "\tturn_on = 1;",
            ""
        ]

        for m in self.models:
            self.__globals__.extend(m.task_sensors_def)
            self.__sensors__.extend(m.task_sensors_eval)
            self.__calls__.extend(m.__calls__)
            self.__layout__.extend(m.task_layout)
            self.__data__.extend(m.__data__)
            self.__dignostics__.extend(m.__diagnostics__)
            self.__monitors__.extend(m.__monitors__)
            # if not m.mon_per is None:
            #     self.__monitors__.append("\tCALL _Monitor"+m.model_name_task+"("+str(m.mon_per)+");")
            # else:
            #     self.__monitors__.append("\tCALL _Monitor"+m.model_name_task+"(_monPer);")
            # if len(m.sensors)>0:
            #     self.__outputs__.append("\t,"+"_sens_"+m.model_name_task)
            self.__events__.extend(m.__events__)
            self.__outputs__.extend(m.__outputs__)
            self.__sets__.extend(m.__sets__)

        self.__monitors__.append("END")
        self.__events__.append("!!eb EVENTs")

        self.__globals__.extend([
            "!!bb General variables",
            "_t0C = 273.15;",
            "_tOffset = _t0C;",
            "_pi = 3.1415927;",
            "_gg = 9.81;",
            "_xgAir(1:4) = 0.,0.,0.757,0.243;",
            "_xgN2(1:4) = 0.,0.,9.999e-1,0.;",
            "_pAtm = 101.3e+03;",
            "_tAtm = 20.+_tOffset;",
            "_tsAtm = WS1P1(1,'P',_pAtm,2);",
            "_kgs = 98066.5;  ! кгс/см2, Па",
            "_MPa = 1.e6; ! МПа, Па",
            "_kPa = 1.e3; ! МПа, Па",
            "_MWt = 1.e6; ! МПа, Па",
            "_kWt = 1.e3; ! МПа, Па",
            "_atm = 101325.; ! атм, Па",
            "_bar = 1.e5; ! бар, Па",
            "_i = 0;",
            "_j = 0;",
            "_m = 0;",
            "_n = 0;",
            "_k = 0;",
            "_x = 0.;",
            "_y = 0.;",
            "_z = 0.;",
            "!!eb General variables",
        ])
        self.__globals__.insert(0, "!!bb Global variables")
        self.__globals__.append("!!eb Global variables")
        self.__calls__.insert(0, "!!bb CALLs")
        self.__calls__.append("!!eb CALLs")
        self.__layout__.insert(0, "LAYOUT")
        self.__layout__.append("END")
        
        self.__sets__.append("SET _CalcSensor;")
        self.__sets__.append("SET _Monitors;")
        self.__sets__.insert(0, "!!bb SETs")
        self.__sets__.append("!!eb SETs")

        self.__main__.extend(self.__layout__)
        self.__main__.extend(self.__calls__)
        self.__main__.extend(self.__sets__)
        self.__main__.extend(self.__outs__)
        self.__main__.insert(0, "MAIN:")
        self.__main__.append("END")

        self.__sensors__.insert(0,"EVENT _CalcSensor")
        self.__sensors__.append("END")

        self.__dignostics__.insert(0, "!!bb Diagnostics")
        self.__dignostics__.append("!!eb Diagnostics")

        self.__outputs__[-1] = self.__outputs__[-1]+";"
        self.__outputs__.insert(0,"OUTPUT _Out")
        self.__outputs__.append("END")
        self.__outputs__.insert(0,"!!bb OUTPUTs")
        self.__outputs__.append("!!eb OUTPUTs")



        self.kordat.extend(self.__task_keys__)
        self.kordat.extend(self.__globals__)
        self.kordat.extend(self.__main__)
        self.kordat.extend(self.__data__)
        self.kordat.extend(self.__dignostics__)
        self.kordat.extend(self.__monitors__)
        self.kordat.extend(self.__sensors__)
        self.kordat.extend(self.__events__)
        self.kordat.extend(self.__outputs__)

    def write_kordat(self, path: str = ""):
        """
        Записать kordat в файл
        
        Arguments
        ----------
        path : str
            Полный путь к файлу зоны задания
        """
        if path == "":
            path = os.path.join(os.path.dirname(os.path.abspath(os.getcwd()))+"\\"+self.task_name+".kor")

        if not os.path.exists(os.path.dirname(os.path.abspath(path))):
            os.mkdir(os.path.dirname(os.path.abspath(path)))

        
        with open(path,'w') as f:
            for line in self.kordat:
                f.write(line+'\n')
