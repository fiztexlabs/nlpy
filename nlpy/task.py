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
            m.rebuild(copy.copy(m.elements), copy.copy(m.model_layout), copy.copy(m.boundary_layout))
            for el in m.elements:
                if el.is_enabled():
                    if el.el_type() == "HCS":
                        mats.extend(el.MAT)
        task_materials = list(set(mats))

        for mat in task_materials:
            self.__globals__.extend(mat.__globals__)



        for m in self.models:
            self.__globals__.extend(m.task_sensors_def)
            self.__sensors__.extend(m.task_sensors_eval)
            self.__calls__.extend(m.__calls__)
            self.__layout__.extend(m.task_layout)
            self.__data__.extend(m.__data__)
            self.__outputs__.append("\t,"+"_sens_"+m.model_name_task)

        self.__globals__.insert(0, "!!bb Global variables")
        self.__globals__.append("!!eb Global variables")
        self.__calls__.insert(0, "!!bb CALLs")
        self.__calls__.append("!!eb CALLs")
        self.__layout__.insert(0, "LAYOUT")
        self.__layout__.append("END")
        
        self.__sets__.append("SET _CalcSensor;")
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

        self.__outputs__[-1] = self.__outputs__[-1]+";"
        self.__outputs__.insert(0,"OUTPUT _Out")
        self.__outputs__.append("END")
        self.__outputs__.insert(0,"!!bb OUTPUTs")
        self.__outputs__.append("!!eb OUTPUTs")



        self.kordat.extend(self.__task_keys__)
        self.kordat.extend(self.__globals__)
        self.kordat.extend(self.__main__)
        self.kordat.extend(self.__data__)
        self.kordat.extend(self.__sensors__)
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
            path = os.path.join("./"+self.task_name+".kor")
            
        with open(path,'w') as f:
            for line in self.kordat:
                f.write(line+'\n')
