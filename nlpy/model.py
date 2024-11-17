import numpy as np
from typing import List
from itertools import count
import copy

from .service import*
from .elements import Element
from .elements import CH
from .elements import HCS
from .elements import BVOL_T
from .elements import SMASS_T
from .elements import BHEAT
from .elements import BLJUN
from .elements import LR

class Model:
    """
    Модель, состоящая из элементов
    =====

    Attributes
    ----------
    id : int
        ID модели (для идентификации нескольких однотипных моделей)

    mon_per : float
        Период обновление мониторов модели

    model_name : str
        имя модели

    task_model_name : str
        имя модели (в задаче)

    elements : List[Element]
        активные элементы модели

    all_elements : List[Element]
        все элементы модели (активные и неактивные)

    elements_submodels : List[Element]
        Активные элементы модели, включая элементы подмоделей

    submodels : List[Model]
        Подмодели
        
    boundary_layout : List[str]
        структура граничных условий модели модели (в нумерации модели)
        
    model_layout : List[str]
        структура модели (в нумерации модели)
        
    task_layout : List[str]
        структура модели (в нумерации задачи)

    Methods
    ----------
    rebuild
        Перестраивает блок DATA элемента
    """

    class Sensor:
        """
        Датчик модели
        =====

        Attributes
        ----------
        expression : str
            Вычисляемое выражение (нумерация элементов соответствует модели)

        Methods
        ----------
        name -> str
            Возвращает имя датчика

        id -> int
            Возвращает ID датчика

        enable
            Включает учет элемента в задаче

        disable
            Выключает учет элемента в задаче

        is_enabled -> bool
            Возвращает True, если элемент включен в задачу и False, если выключен
        """
        _ids = count(1)
        def __init__(
                self,
                name: str,
                expression: str
            ):
            self.__name__ = name
            self.expression = expression
            self.__id__ = next(self._ids)

            # enable (True) or disable (False) this sensor to the task
            self.__enable_in_task__ = True

        def name(self) -> str:
            """
            Имя датчика
            """
            return self.__name__
        
        def id(self) -> int:
            """
            ID датчика
            """
            return self.__id__
        
        def enable(self):
            """
            Включить датчик модели в задаче
            """
            self.__enable_in_task__ = True

        def disable(self):
            """
            Выключить датчик модели в задаче
            """
            self.__enable_in_task__ = False

        def is_enabled(self) -> bool:
            """
            Сообщает, включен ли данный датчик в задачу
            """
            return self.__enable_in_task__

    def __init__(
        self,
        # orig = None,
        **kwargs
        ):
        """
        Конструктор
        
        Arguments
        ----------
        orig : Model (optional)
            Объект для копирования 

        name : str (optional)
            Имя модели. По умолчанию Mdl

        model_layout : List[str] (optional)
            Струтктура модели (в нумерациии модели)

        boundary_layout : List[str] (optional)
            Струтктура граничных условий модели (в нумерациии модели)

        elements : List[Element] (optional)
            Элементы модели

        sensors : List[Sensor] (optional)
            Все датчики модели (в нумерации модели)

        active_sensors : List[Sensor] (optional)
            Активные датчики модели (в нумерации модели)

        task_sensors : List[Sensor] (optional)
            Активные датчики модели (в нумерации задачи)

        """
        
        self.Sensor._ids = count(1)

        self.mon_per = None

        self.all_elements = []
        self.elements = []
        self.elements_submodels = []
        self.model_layout = []
        self.boundary_layout = []
        self.task_layout = []
        self.task_sensors_def = []
        self.task_sensors_eval = []

        self.sensors = []
        self.active_sensors = []

        self.__calls__ = []
        self.__sets__ = []
        self.__data__ = []
        self.__sensors__ = []
        self.__sens_eval__ = []

        self.id = kwargs['id']
        if kwargs['name'] == "":
            self.model_name = "Mdl"
        else:
            self.model_name = kwargs['name']
        self.model_name_task = self.model_name+str(self.id)
        self.__constructor__(kwargs)

        # if orig is None:
        #     self.id = kwargs['id']
        #     if kwargs['name'] == "":
        #         self.model_name = "Mdl"
        #     else:
        #         self.model_name = kwargs['name']
        #     self.model_name_task = self.model_name+str(self.id)
        #     self.__constructor__(kwargs)
        # else:
        #     self.__copy_constructor__(orig)

    def __constructor__(self, kwargs):
        elements = []
        sensors = []
        submodels = []
        boundary_layout = []
        model_layout = []
        submodel_links_layout = []
        if 'boundary_layout' in kwargs:
            boundary_layout = kwargs['boundary_layout']
        if 'model_layout' in kwargs:
            model_layout = kwargs['model_layout']
        if 'elements' in kwargs:
            elements = kwargs['elements']
        if 'sensors' in kwargs:
            sensors = kwargs['sensors']
        if 'submodels' in kwargs:
            submodels = kwargs['submodels']
        if 'submodel_links_layout' in kwargs:
            submodel_links_layout = kwargs['submodel_links_layout']

        self.rebuild(
            elements=elements, 
            model_layout=model_layout, 
            boundary_layout=boundary_layout, 
            sensors=sensors, 
            submodels=submodels,
            submodel_links_layout=submodel_links_layout
        )

    # def __copy_constructor__(self, orig):
    #     self.model_name = orig.model_name
    #     self.model_name_task = self.model_name+str(self.id)
    #     self.id = next(orig.ids)
    #     self.__constructor__(
    #         {
    #             'elements' : [eval(el.el_type()+"(el)") for el in orig.elements],
    #             'model_layout' : orig.model_layout,
    #             'boundary_layout' : orig.boundary_layout,
    #             'sensors' : orig.sensors,
    #             'submodels': orig.submodels
    #         })

    def __layout__(self, model_layout: List[str], boundary_layout: List[str], submodel_links_layout: List[str]):
        """
        Сгенерировать структуру модели для kordat
        """
        self.task_layout = []
        self.boundary_layout = boundary_layout
        self.model_layout = model_layout
        self.submodel_links_layout = submodel_links_layout

        # read links between submodels
        links = copy.deepcopy(submodel_links_layout)
        if len(links) > 0:
            for line in links:
                self.task_layout.append(line)
                for sm in self.submodels:
                    disabled_elements = 0
                    for el in sm.all_elements:
                        if sm.model_name_task+"."+el.el_type()+str(el.id_model) in line:
                            self.task_layout[-1] = self.task_layout[-1].replace(sm.model_name_task+"."+el.el_type()+str(el.id_model), el.name())
                            if not el.is_enabled():
                                disabled_elements+=1
                    if disabled_elements > 0:
                        self.task_layout[-1] = "! "+self.task_layout[-1]

        self.task_layout.insert(0,"!!bb link submodels")
        self.task_layout.append("!!eb link submodels")

        layout = copy.deepcopy(boundary_layout)
        layout.insert(0, "!!bb boundaries")
        layout.append("!!eb boundaries")
        layout.append("!!bb model")
        layout.extend(model_layout)
        layout.append("!!eb model")

        if len(layout) > 0:
            for line in layout:
                self.task_layout.append(line)
                disabled_elements = 0
                for el in self.all_elements:
                    if el.el_type()+str(el.id_model) in line:
                        self.task_layout[-1] = self.task_layout[-1].replace(el.el_type()+str(el.id_model), el.name())
                        if not el.is_enabled():
                            disabled_elements+=1
                if disabled_elements > 0:
                    self.task_layout[-1] = "! "+self.task_layout[-1]

        self.task_layout.insert(0, "!!bb Lay "+self.model_name_task)
        self.task_layout.append("!!eb Lay "+self.model_name_task)
    
    def __set_sensors__(self, sensors: List[Sensor]):
        self.sensors = sensors
        self.active_sensors = []
        self.task_sensors_eval = []
        self.task_sensors_def = []
        self.__sensors__ = []
        self.__sens_eval__ = []

        if len(self.sensors) > 0:
            # fill sensor's array
            for sens in self.sensors:
                self.__sensors__.append("_sens_"+self.model_name_task+"("+str(sens.id())+")=")
                if sens.is_enabled():
                    self.active_sensors.append(sens)
                    self.__sensors__[-1]+=sens.expression
                else:
                    self.__sensors__[-1]+="0.;"
            # replace model numeration by task numeration
            for line in self.__sensors__:
                self.__sens_eval__.append(line)
                disabled_elements = 0
                for el in self.all_elements:
                    if el.el_type()+str(el.id_model) in line:
                        self.__sens_eval__[-1] = self.__sens_eval__[-1].replace(el.el_type()+str(el.id_model), el.name())
                        if not el.is_enabled():
                            disabled_elements+=1
                if disabled_elements > 0:
                    self.__sens_eval__[-1] = "_sens_"+self.model_name_task+"("+str(sens.id())+")=0.;"

            self.task_sensors_eval = []
            self.task_sensors_eval.extend(self.__sens_eval__)
            self.task_sensors_eval.insert(0,"!!bb Sensors "+self.model_name_task)
            self.task_sensors_eval.append("!!eb Sensors "+self.model_name_task)

            self.task_sensors_def = []
            self.task_sensors_def.append("!!bb Sensors "+self.model_name_task)
            self.task_sensors_def.append("_sens_"+self.model_name_task+"(1:"+str(next(copy.copy(self.Sensor._ids))-1)+")=0.;")
            self.task_sensors_def.append("!!eb Sensors "+self.model_name_task)

    def __ch_compiletime_diag__(self):
        if len(self.ch) > 0:
            task_ch_nums = []
            model_ch_nums = []
            ch_cells_nums = []
            for ch in self.ch:
                model_ch_nums.append(ch.id_model)
                task_ch_nums.append(ch.id)
                ch_cells_nums.append(ch.N)

            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                task_ch_nums, 
                "_ch"+self.model_name_task,
                "(1:"+str(len(task_ch_nums))+")",
                ":=",
                "\t\t"
            ))
            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                model_ch_nums, 
                "_chLay"+self.model_name_task,
                "(1:"+str(len(model_ch_nums))+")",
                ":=",
                "\t\t"
            ))
            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                ch_cells_nums, 
                "_chN"+self.model_name_task,
                "(1:"+str(len(ch_cells_nums))+")",
                ":=",
                "\t\t"
            ))

            self.__compiletime_diagnostics__.extend(
                [
                    "\t\tPRINT '*** CH DATA "+self.model_name_task+" ***';",
                    "\t\tDO _i=1,"+str(len(self.ch))+";",
                    "\t\t\t_m=_ch"+self.model_name_task+"(_i);",
                    "\t\t\t_n=_chLay"+self.model_name_task+"(_i);",
                    "\t\t\tPRINT '- CH',_m,' in model "+self.model_name_task+" ',_n;",
                    "\t\t\t! Геометрия каналов",
                    "\t\t\t_fullLen := 0.; _fullLen = 0.;  ! Full length\t ",
                    "\t\t\t_fullHgt := 0.; _fullHgt = 0.;  ! Full height dif",
                    "\t\t\t_fullVol := 0.; _fullVol = 0.;  ! Full volume\t ",
                    "\t\t\tPRINT 'Cl','----- DZ ------','----- DH ------','----- V -------',",
                    "\t\t\t\t'----- PR ------';",
                    "\t\t\tDO _j=1,N.CH(_m);",
                    "\t\t\t\t_fullLen = _fullLen + DZ.CH(_m)(_j);",
                    "\t\t\t\t_fullHgt = _fullHgt + DH.CH(_m)(_j);",
                    "\t\t\t\t_fullVol = _fullVol + V.CH(_m)(_j);",
                    "\t\t\t\tPRINT _j,DZ.CH(_m)(_j),DH.CH(_m)(_j),V.CH(_m)(_j),PR.CH(_m)(_j);",
                    "\t\t\tENDDO",
                    "\t\t\tPRINT 'Cl','----- S -------','----- D -------','---- Type -----',",
                    "\t\t\t\t'----- DэквS ---';",
                    "\t\t\tDO _j=1,N.CH(_m);",
                    "\t\t\t\tPRINT _j,S.CH(_m)(_j),D.CH(_m)(_j),TYPE.CH(_m)(_j),'\t\t\t\t ',",
                    "\t\t\t\t ((4*S.CH(_m)(_j))/_pi)**0.5;",
                    "\t\t\tENDDO",
                    "\t\t\tPRINT 'Jc','---- DZJ ------','---- SJ -------','---- JUN ------',",
                    "\t\t\t\t'---- DэквSJ ---';",
                    "\t\t\tDO _j=1,N.CH(_m)+1;",
                    "\t\t\t\tPRINT _j,DZJ.CH(_m)(_j),SJ.CH(_m)(_j),JUN.CH(_m)(_j),'\t\t\t\t ',",
                    "\t\t\t\t ((4*SJ.CH(_m)(_j))/_pi)**0.5;",
                    "\t\t\tENDDO",
                    "\t\t\tIF _diag > 1 THEN ! вывод исходных значений",
                    "\t\t\t\tPRINT 'Cl','----- P -------','----- T1 ------','---- T2 -------';",
                    "\t\t\t\tDO _j=1,N.CH(_m);",
                    "\t\t\t\t PRINT _j,P.CH(_m)(_j),T.CH(_m)(1,_j)-_tOffset,",
                    "\t\t\t\t\tT.CH(_m)(2,_j)-_tOffset;",
                    "\t\t\t\tENDDO",
                    "\t\t\t\tPRINT 'Cl','----- VOID ----','----- XNG3 ----','---- XNG4 -----';",
                    "\t\t\t\tDO _j=1,N.CH(_m);",
                    "\t\t\t\t\tPRINT _j,VOID.CH(_m)(_j),XNG.CH(_m)(3,_j),XNG.CH(_m)(4,_j);",
                    "\t\t\t\tENDDO",
                    "\t\t\t\tPRINT 'Cl','----- XNF3 ----','---- XNF4 -----','---------------';",
                    "\t\t\t\tDO _j=1,N.CH(_m);",
                    "\t\t\t\t\tPRINT _j,XNF.CH(_m)(3,_j),XNF.CH(_m)(4,_j);",
                    "\t\t\t\tENDDO",
                    "\t\t\tENDIF",
                    "\t\t\tPRINT '---------------------------------------------------';",
                    "\t\t\tPRINT 'Full length\t ',_fullLen;",
                    "\t\t\tPRINT 'Full height dif',_fullHgt;",
                    "\t\t\tPRINT 'Full volume\t ',_fullVol;",
                    "\t\tENDDO",
                    "\t\tPRINT ' ';"
                ]
            )

    def __hcs_compiletime_diag__(self):
        if len(self.hcs) > 0:
            task_hcs_nums = []
            model_hcs_nums = []
            hcs_cells_nums = []
            for hcs in self.hcs:
                model_hcs_nums.append(hcs.id_model)
                task_hcs_nums.append(hcs.id)
                hcs_cells_nums.append(hcs.N)

            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                task_hcs_nums, 
                "_hcs"+self.model_name_task,
                "(1:"+str(len(task_hcs_nums))+")",
                ":=",
                "\t\t"
            ))
            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                model_hcs_nums, 
                "_hcsLay"+self.model_name_task,
                "(1:"+str(len(model_hcs_nums))+")",
                ":=",
                "\t\t"
            ))
            self.__compiletime_diagnostics__.extend(fill_korsar_array(
                hcs_cells_nums, 
                "_hcsN"+self.model_name_task,
                "(1:"+str(len(hcs_cells_nums))+")",
                ":=",
                "\t\t"
            ))

            self.__compiletime_diagnostics__.extend(
                [
                    "\t\tPRINT '*** HCS DATA "+self.model_name_task+" ***';",
                    "\t\tDO _i=1,"+str(len(self.hcs))+";",
                    "\t\t\t_m=_hcs"+self.model_name_task+"(_i);",
                    "\t\t\t_n=_hcsLay"+self.model_name_task+"(_i);",
                    "\t\t\tPRINT '- HCS',_m,' in model "+self.model_name_task+" ',_n;",
                    "\t\t\t! Геометрия ТК",
                    "\t\t\t_dzFullHcs"+self.model_name_task+" := 0.;",
                    "\t\t\t_f1FullHcs"+self.model_name_task+" := 0.;",
                    "\t\t\t_f2FullHcs"+self.model_name_task+" := 0.;",
                    "\t\t\tPRINT 'Cl','----- DFZ ----- ','----- DF1 ----- ','---- DF2 ------';",
                    "\t\t\t\tDO _j=1,N.HCS(_m);",
                    "\t\t\t\t\t_dzFullHcs"+self.model_name_task+" = _dzFullHcs"+self.model_name_task+" + DFZ.HCS(_m)(_j);",
                    "\t\t\t\t\t_f1FullHcs"+self.model_name_task+" = _f1FullHcs"+self.model_name_task+" + DF.HCS(_m)(1,_j);",
                    "\t\t\t\t\t_f2FullHcs"+self.model_name_task+" = _f2FullHcs"+self.model_name_task+" + DF.HCS(_m)(2,_j);",
                    "\t\t\t\t\tPRINT _j,DFZ.HCS(_m)(_j),DF.HCS(_m)(1,_j),DF.HCS(_m)(2,_j);",
                    "\t\t\t\tENDDO",
                    "\t\t\tPRINT '---------------------------------------------------';",
                    "\t\t\tPRINT 'Full length      ',_dzFullHcs"+self.model_name_task+";",
                    "\t\t\tPRINT 'Surf 1 area      ',_f1FullHcs"+self.model_name_task+";",
                    "\t\t\tPRINT 'Surf 2 area      ',_f2FullHcs"+self.model_name_task+";",
                    "\t\t\tPRINT 'Geom mult B      ',B.HCS(_m);",
                    "\t\t\tPRINT 'Coeff. ALM-1     ',ALM.HCS(_m)(1);",
                    "\t\t\tPRINT 'Coeff. ALM-2     ',ALM.HCS(_m)(2);",
                    "\t\tENDDO",
                    "\t\tPRINT ' ';",
                ]
            )

    def __ch_runtime_diag__(self):
        if len(self.ch) > 0:
            self.__runtime_diagnostics__.extend([
                "\t\tPRINT '=== CH DATA "+self.model_name_task+" ===';",
                "\t\tDO _i=1,"+str(len(self.ch))+";",
                "\t\t\t_k=_ch"+self.model_name_task+"(_i);",
                "\t\t\t_n=_chLay"+self.model_name_task+"(_i);",
                "\t\t\tPRINT ' TAU = ',TAU,'\tDT = ',DT;",
                "\t\t\tPRINT '- CH',_k,' in model "+self.model_name_task+"',_n;",
                "\t\t\tPRINT 'Cl','----- P -------','---- VOID -----','---- T1 -------',",
                "\t\t\t\t'---- DEN1 ------';",
                "\t\t\t_mCh := 0.; _mCh = 0.;",
                "\t\t\tDO _j=1,N.CH(_k);",
                "\t\t\t\t! Расчет массы канала",
                "\t\t\t\t_mCh = _mCh + ",
                "\t\t\t\t\tV.CH(_k)(_j)*( VOID.CH(_k)(_j)*DEN.CH(_k)(2,_j) + ",
                "\t\t\t\t\t(1.-VOID.CH(_k)(_j))*DEN.CH(_k)(1,_j) );",
                "\t\t\t\tPRINT _j,P.CH(_k)(_j),VOID.CH(_k)(_j),T.CH(_k)(1,_j)-_tOffset,",
                "\t\t\t\t\tDEN.CH(_k)(1,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Cl','---- T2 -------','---- DEN2 ------','---- XNG3 -----',",
                "\t\t\t\t'---- XNG4 -----';",
                "\t\t\tDO _j=1,N.CH(_k);",
                "\t\t\t\tPRINT _j,T.CH(_k)(2,_j)-_tOffset,DEN.CH(_k)(2,_j),XNG.CH(_k)(3,_j),",
                "\t\t\t\t\tXNG.CH(_k)(4,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Jc','---- CFLw -----','---- CFLs -----';",
                "\t\t\tDO _j=1,N.CH(_k)+1;",
                "\t\t\t\tIF(\"($W.CH(_k)(1,_j),1) < -1.e-13 | ",
                "\t\t\t\t\t\"($W.CH(_k)(1,_j),1) > 1.e-13) THEN",
                "\t\t\t\t\t_x = DT*W.CH(_k)(1,_j)/DZJ.CH(_k)(_j);",
                "\t\t\t\tELSE",
                "\t\t\t\t\t_x = -888.;",
                "\t\t\t\tENDIF",
                "\t\t\t\tIF(\"($W.CH(_k)(2,_j),2) < -1e-13 | ",
                "\t\t\t\t\t\"($W.CH(_k)(2,_j),2) > 1e-13) THEN",
                "\t\t\t\t\t_y = DT*W.CH(_k)(2,_j)/DZJ.CH(_k)(_j);",
                "\t\t\t\tELSE",
                "\t\t\t\t\t_y = -888.;",
                "\t\t\t\tENDIF",
                "\t\t\t\tPRINT _j,_x,_y;",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Jc','---- Gwater ---','---- Gsteam ---','---- Gmix -----',",
                "\t\t\t\t'---- FRWw -----';",
                "\t\t\tDO _j=1,N.CH(_k)+1;",
                "\t\t\t\tPRINT _j,\"($W.CH(_k)(1,_j),1),\"($W.CH(_k)(2,_j),2),",
                "\t\t\t\t\t\"($W.CH(_k)(1,_j),1) + \"($W.CH(_k)(2,_j),2),",
                "\t\t\t\t\tW.CH(_k)(1,_j)*FRW.CH(_k)(1,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Jc','---- Wwater ---','---- Wsteam ---','---- MAPJ -----',",
                "\t\t\t\t'---- FRWs -----';",
                "\t\t\tDO _j=1,N.CH(_k)+1;",
                "\t\t\t\tPRINT _j,W.CH(_k)(1,_j),W.CH(_k)(2,_j),MAPJ.CH(_k)(_j),",
                "\t\t\t\t\t'\t\t\t\t\t\t\t',W.CH(_k)(2,_j)*FRW.CH(_k)(2,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT '-- Mass CH = ',_mCh;",
                "\t\tENDDO\t",
                "\t\tPRINT ' ';"
            ])

    def __hcs_runtime_diag__(self):
        if len(self.hcs) > 0:
            self.__runtime_diagnostics__.extend([
                "\t\tPRINT '=== HCS DATA "+self.model_name_task+" ===';",
                "\t\tDO _i=1,"+str(len(self.hcs))+";",
                "\t\t\t_k=_hcs"+self.model_name_task+"(_i);",
                "\t\t\t_n=_hcsLay"+self.model_name_task+"(_i);",
                "\t\t\tPRINT ' TAU = ',TAU,'\tDT = ',DT;",
                "\t\t\tPRINT '- HCS',_k,' in model "+self.model_name_task+"',_n;",
                "\t\t\tPRINT 'Cl','----- Tw1 -----','---- Tw2 ------','---- ALW1 -----';",
                "\t\t\tDO _j=1,N.HCS(_k);",
                "\t\t\t\tPRINT _j,TW.HCS(_k)(1,_j)-_tOffset,TW.HCS(_k)(2,_j)-_tOffset,",
                "\t\t\t\t\tALW.HCS(_k)(1,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Cl','---- ALW2 -----','---- Qw1-1 ----','---- Qw1-2 ----';",
                "\t\t\t_x = 0.;_y = 0.;  ! Мощности",
                "\t\t\tDO _j=1,N.HCS(_k);",
                "\t\t\t\t_x = _x + QW.HCS(_k)(1,_j)+QW.HCS(_k)(2,_j);",
                "\t\t\t\t_y = _y + QW.HCS(_k)(3,_j)+QW.HCS(_k)(4,_j);",
                "\t\t\t\tPRINT _j,ALW.HCS(_k)(2,_j),QW.HCS(_k)(1,_j),QW.HCS(_k)(2,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Cl','---- Qw2-1 ----','---- Qw2-2 ----','---- Mod1 -----';",
                "\t\t\tDO _j=1,N.HCS(_k);",
                "\t\t\t\tPRINT _j,QW.HCS(_k)(3,_j),QW.HCS(_k)(4,_j),MOD.HCS(_k)(1,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Cl','---- QR1 ------','---- QR2 ------','---- Mod2 -----';",
                "\t\t\tDO _j=1,N.HCS(_k);",
                "\t\t\t\tPRINT _j,QR.HCS(_k)(1,_j),QR.HCS(_k)(2,_j),MOD.HCS(_k)(2,_j);",
                "\t\t\tENDDO",
                "\t\t\tPRINT 'Total power Qw/1, Qw/2:',_x,_y;",
                "\t\tENDDO",
                "\t\tPRINT ' ';"
            ])

    def __set__compiletime_diagnostics__(self):

        self.__compiletime_diagnostics__ = [
            "\t! Диагностика геометрии",
            "\tIF first THEN",
            "\t\tfirst = 0;",
            "\t\t_cntr"+self.model_name_task+" := 0.;",
            "\t\tPRINT '*** Сводные данные по "+self.model_name_task+" ***';",
            "\t\tPRINT '=== MODEL "+self.model_name_task+" GEOMETRY DIAGNOSTICS ===';",
        ]
        
        self.__ch_compiletime_diag__()
        self.__hcs_compiletime_diag__()
        
        self.__compiletime_diagnostics__.extend([
            "\t\tPRINT '=== MODEL "+self.model_name_task+" GEOMETRY DIAGNOSTICS END ===';",
            "\tENDIF"
        ])

    def __set__runtime_diagnostics__(self):
        self.__runtime_diagnostics__ = [
            "",
            "\t! инкремент счетчика",
            "\tIF _cntr"+self.model_name_task+"<=_dt"+self.model_name_task+" THEN",
            "\t\t_cntr"+self.model_name_task+" = _cntr"+self.model_name_task+"+DT;",
            "\tELSE",
            "\t\t_cntr"+self.model_name_task+" = 0.;",
            "\tENDIF",
            "",
            "\tIF _cntr"+self.model_name_task+"==0. THEN ! выполнение процедуры",
            "\t\tPRINT '=== MODEL "+self.model_name_task+" CALCULATION DIAGNOSTICS ===';",
            "\t\tPRINT 'TAU = ',TAU,'  DT = ',DT;",
        ]

        self.__ch_runtime_diag__()
        self.__hcs_runtime_diag__()

        self.__runtime_diagnostics__.append("\tENDIF")

    def __set_diagnostics__(self):
        self.__sets__.append("SET "+"_Monitor"+self.model_name_task+";")

        self.__diagnostics__ = [            
            "EVENT _Monitor"+self.model_name_task+"(_dt"+self.model_name_task+")",
            "\treplace = 1;",
            "\tturn_on = 1;"
        ]

        self.ch = []
        self.hcs = []
        self.lr = []
        for el in self.elements:
            if el.el_type() == "CH":
                self.ch.append(el)
            if el.el_type() == "HCS":
                self.hcs.append(el)
            if el.el_type() == "LR":
                self.lr.append(el)

        self.__set__compiletime_diagnostics__()

        self.__diagnostics__.extend(self.__compiletime_diagnostics__)

        self.__set__runtime_diagnostics__()

        self.__diagnostics__.extend(self.__runtime_diagnostics__)

        self.__diagnostics__.extend(["END"])


    def rebuild(
            self,
            **kwargs
        ):
        """
        Перестроить зону задания модели (блоки DATAs, CALLs, LAYOUT, OUTPUTs, а также сенсоры и процедуры)

        Arguments
        ----------
        elements : List[Element]
            Элементы модели

        model_layout : List[str]
            Структура модели

        boundary_layout : List[str]
            Структура ГУ модели

        submodel_links_layout : List[str]
            Структура соединений подмоделей

        sensors : List[Model.Sensor]
            Датчики
            
        submodels : List[Model]
            Подмодели

        """
        
        elements = kwargs['elements']
        model_layout = kwargs['model_layout']
        boundary_layout = kwargs['boundary_layout']
        submodel_links_layout = kwargs['submodel_links_layout']
        sensors = kwargs['sensors']
        submodels = kwargs['submodels']
        
        
        self.submodels = submodels
        self.elements = []
        self.all_elements = []

        self.__calls__ = []
        self.__data__ = []
        self.__sets__ = []
        self.__outputs__ = []
        self.__monitors__ = []

        if len([elements]) > 0:
            i_ch = 1
            i_hcs = 1
            i_lr = 1
            i_bv = 1
            i_sm = 1
            i_bh = 1
            i_blj = 1
            for el in elements:
                self.all_elements.append(el)
                if (el.el_type() == "HCS"):
                    el.id_model = i_hcs
                    i_hcs += 1
                if (el.el_type() == "CH"):
                    el.id_model = i_ch
                    i_ch += 1
                if (el.el_type() == "LR"):
                    el.id_model = i_lr
                    i_lr += 1
                if (el.el_type() == "BVOL_T"):
                    el.id_model = i_bv
                    i_bv += 1
                if (el.el_type() == "SMASS_T"):
                    el.id_model = i_sm
                    i_sm += 1
                if (el.el_type() == "BHEAT"):
                    el.id_model = i_bh
                    i_bh += 1
                if (el.el_type() == "BLJUN"):
                    el.id_model = i_blj
                    i_blj += 1
                if el.is_enabled():
                    self.elements.append(el)

                    el.__model_name__ = self.model_name_task

                    self.__calls__.append("CALL "+el.name()+";")
                    self.__data__.extend(el.__data__)

        self.elements_submodels = self.elements

        self.__calls__.insert(0, "!!bb CALLs "+self.model_name_task)
        self.__calls__.append("!!eb CALLs "+self.model_name_task)

        self.__data__.insert(0, "!!bb DATAs "+self.model_name_task)
        self.__data__.append("!!eb DATAs "+self.model_name_task)

        self.__layout__(model_layout, boundary_layout, submodel_links_layout)

        self.__set_sensors__(sensors)
        if len(sensors)>0:
            self.__outputs__.append("\t,"+"_sens_"+self.model_name_task)
        if not self.mon_per is None:
            self.__monitors__.append("\tCALL _Monitor"+self.model_name_task+"("+str(self.mon_per)+");")
        else:
            self.__monitors__.append("\tCALL _Monitor"+self.model_name_task+"(_monPer);")

        self.__set_diagnostics__()
        self.__sets__.insert(0, "!!bb SETs "+self.model_name_task)
        self.__sets__.append("!!eb SETs "+self.model_name_task)

        if len(submodels) > 0:
            for m in submodels:
                m.rebuild(
                    elements=copy.copy(m.all_elements), 
                    model_layout=copy.copy(m.model_layout), 
                    boundary_layout=copy.copy(m.boundary_layout), 
                    sensors=copy.copy(m.sensors), 
                    submodels=copy.copy(m.submodels),
                    submodel_links_layout=copy.copy(m.submodel_links_layout)
                )
                self.__calls__ = m.__calls__ + self.__calls__
                self.__data__ = m.__data__ + self.__data__
                self.__sets__ = m.__sets__ + self.__sets__
                self.__diagnostics__ = m.__diagnostics__ + self.__diagnostics__
                self.elements_submodels = m.elements_submodels + self.elements_submodels
                self.task_layout = m.task_layout + self.task_layout
                self.task_sensors_def = m.task_sensors_def + self.task_sensors_def
                self.task_sensors_eval = m.task_sensors_eval + self.task_sensors_eval
                self.__outputs__ = m.__outputs__ + self.__outputs__
                self.__monitors__ = m.__monitors__ + self.__monitors__

    