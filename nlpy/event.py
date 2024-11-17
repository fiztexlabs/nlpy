from .model import Model
from .task import Task

from typing import List, Union
from itertools import count
import copy

class Event:
    ids = count(1)
    def __init__(
            self,
            name: str,
            TYPE: int,
            TURN_ON: bool,
            parent: Union[List[Model], Task],
            layout: List[str],
            arguments: List[str] = []

    ):
        self.id=next(self.ids)
        self.name = name
        self.task_name = name+str(self.id)
        self.TYPE = TYPE
        self.TURN_ON = TURN_ON
        self.arguments = arguments
        self.init_layout = layout

        self.task_layout = []
        self.task_arguments = []

        self.__enable_in_task__ = True

        if type(parent) == Task:
            self.models = parent.models
        if type(parent) == list:
            self.models = parent
        
        if len(self.models) == 1:
            self.task_name = name+self.models[0].model_name_task


        if len(self.arguments) > 0:
            self.task_layout.append("EVENT "+self.task_name+"(")
            for a in self.arguments:
                self.task_arguments.append(a+str(id))
                self.task_layout[-1] = self.task_layout[-1]+self.task_arguments[-1]+","
            self.task_layout[-1] = self.task_layout[-1][0:-1]+")"
        else:
            self.task_layout.extend([
                "EVENT "+self.task_name,
                "\ttype = "+str(self.TYPE)+";"
            ])
        
        self.task_layout.extend([
            "\treplace = 1;",
            "\tturn_on = "+str(self.TURN_ON)+";"
        ])
        
        layout = copy.deepcopy(self.init_layout)
        if len(layout) > 0:
            if len(self.models) > 1:
                for line in layout:
                    self.task_layout.append(line)
                    for m in self.models:
                        disabled_elements = 0
                        for el in m.all_elements:
                            if m.model_name_task+"."+el.el_type()+str(el.id_model) in line:
                                self.task_layout[-1] = self.task_layout[-1].replace(m.model_name_task+"."+el.el_type()+str(el.id_model), el.name())
                                if not el.is_enabled():
                                    disabled_elements+=1
                        if disabled_elements > 0:
                            self.task_layout[-1] = "! "+self.task_layout[-1]
            if len(self.models) == 1:
                for line in layout:
                    self.task_layout.append(line)
                    disabled_elements = 0
                    for el in self.models[0].all_elements:
                        if el.el_type()+str(el.id_model) in line:
                            self.task_layout[-1] = self.task_layout[-1].replace(el.el_type()+str(el.id_model), el.name())
                            if not el.is_enabled():
                                disabled_elements+=1
                    if disabled_elements > 0:
                        self.task_layout[-1] = "! "+self.task_layout[-1]
            
        self.task_layout.append("END")

    def enable(self):
        """
        Включить EVENT в задачу
        """
        self.__enable_in_task__ = True

    def disable(self):
        """
        Выключить EVENT из задачи
        """
        self.__enable_in_task__ = False

    def is_enabled(self) -> bool:
        """
        Сообщает, включен ли данный EVENT в задачу
        """
        return self.__enable_in_task__

        

