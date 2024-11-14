import numpy as np
from typing import List
from itertools import count
import copy

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

    model_name : str
        имя модели

    task_model_name : str
        имя модели (в задаче)

    elements : List[Element]
        активные элементы модели

    all_elements : List[Element]
        все элементы модели (активные и неактивные)
        
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

    _ids = count(1)

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
        orig = None,
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
        self.id = next(self._ids)
        self.Sensor._ids = count(1)

        self.all_elements = []
        self.elements = []
        self.model_layout = []
        self.boundary_layout = []
        self.task_layout = []
        self.task_sensors_def = []
        self.task_sensors_eval = []

        self.sensors = []
        self.active_sensors = []

        self.__calls__ = []
        self.__data__ = []
        self.__sensors__ = []
        self.__sens_eval__ = []

        if orig is None:
            if kwargs['name'] == "":
                self.model_name = "Mdl"
            else:
                self.model_name = kwargs['name']
            self.model_name_task = self.model_name+str(self.id)
            self.__constructor__(kwargs)
        else:
            self.__copy_constructor__(orig)


    def __constructor__(self, kwargs):
        elements = []
        sensors = []
        boundary_layout = []
        model_layout = []
        if 'boundary_layout' in kwargs:
            boundary_layout = kwargs['boundary_layout']
        if 'model_layout' in kwargs:
            model_layout = kwargs['model_layout']
        if 'elements' in kwargs:
            elements = kwargs['elements']
        if 'sensors' in kwargs:
            sensors = kwargs['sensors']

        self.rebuild(elements, model_layout, boundary_layout, sensors)
        

    def __copy_constructor__(self, orig):
        self.model_name = orig.model_name
        self.model_name_task = self.model_name+str(self.id)
        self.__constructor__(
            {
                'elements' : [eval(el.el_type()+"(el)") for el in orig.elements],
                'model_layout' : orig.model_layout,
                'boundary_layout' : orig.boundary_layout,
                'sensors' : orig.sensors
            })

    def __layout__(self, model_layout: List[str], boundary_layout: List[str]):
        """
        Сгенерировать структуру модели для kordat
        """
        self.task_layout = []
        self.boundary_layout = boundary_layout
        self.model_layout = model_layout

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

    def rebuild(self, elements: List[Element], model_layout: List[str], boundary_layout: List[str], sensors: List[Sensor] = []):
        """
        Перестроить блоки LAYOUT, CALLs и DATA, а также датчики модели
        """
        self.elements = []
        self.all_elements = []

        self.__calls__ = []
        self.__data__ = []

        if len(elements) > 0:
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


        self.__calls__.insert(0, "!!bb CALLs "+self.model_name_task)
        self.__calls__.append("!!eb CALLs "+self.model_name_task)

        self.__data__.insert(0, "!!bb DATAs "+self.model_name_task)
        self.__data__.append("!!eb DATAs "+self.model_name_task)

        self.__layout__(model_layout, boundary_layout)
        self.__set_sensors__(sensors)

    