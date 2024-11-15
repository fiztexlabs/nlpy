import os
from ..service import*

class Element:
    """
    Обобщенный элемент нодализационной схемы
    =====

    Attributes
    ----------
    id : int
        ID элемента (нумерация задачи)
        
    id_model : int
        ID элемента (нумерация модели)

    Methods
    ----------
    type -> str
        Возвращает тип элемента

    name -> str
        Возвращает имя элемента

    model_name -> str
        Возвращает имя модели, к которой принадлежит элемент

    enable
        Включает учет элемента в задаче

    disable
        Выключает учет элемента в задаче

    is_enabled -> bool
        Возвращает True, если элемент включен в задачу и False, если выключен
    """

    def __init__(self):
        # element type
        self.__type__ = ""

        # global element id
        self.id = 0

        # element name
        self.__name__ = ""

        # text for DATA kordat
        self.__data__ = []

        # name of model, which own this element
        self.__model_name__ = ""

        # enable (True) or disable (False) this element to the task
        self.__enable_in_task__ = True

        # model id
        self.id_model = self.id

    def __write_data__(self, path: str = ""):
        """
        Записать блок DATA элемента в файл
        
        Arguments
        ----------
        path : str
            Полный путь к файлу зоны задания
        """
        if path == "":
            path = os.path.join("./"+self.__name__+".txt")

        write_data(self.__data__,path)

    def enable(self):
        """
        Включить граничное условие модели в задачу
        """
        self.__enable_in_task__ = True

    def disable(self):
        """
        Выключить граничное условие из задачи
        """
        self.__enable_in_task__ = False

    def is_enabled(self) -> bool:
        """
        Сообщает, включено ли данное граничное условие в задачу
        """
        return self.__enable_in_task__
    
    def el_type(self) -> str:
        """
        Тип элемента
        """
        return self.__type__
        
    def name(self) -> str:
        """
        Имя элемента
        """
        return self.__name__
        
    def model_name(self) -> str:
        """
        Имя модели элемента
        """
        return self.__model_name__

    def rebuild(self):
        """
        Перестроить kordat элемента
        """
        raise NotImplementedError()

