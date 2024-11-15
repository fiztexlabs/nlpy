from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class BLJUN(Element):
    """
    Элемент непроницаемое соединение
    =====

    Attributes
    ----------
    TYPE : int
        Тип

    Methods
    ----------
    rebuild
        Перестраивает блок DATA элемента
    
    """

    _ids = count(1)

    def __init__(
        self,
        orig = None,
        model_name = "",
        **kwargs
    ):
        Element.__init__(self)

        self.id = next(self._ids)

        self.__type__ = "BLJUN"
        self.typepp = self
        self.__name__ = "BLJUN"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['TYPE']
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.TYPE
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        TYPE: int
    ):
        self.TYPE = np.array(fill_list_or_float(TYPE,1),dtype=int)

    def rebuild(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.extend(fill_korsar_array(self.TYPE, "TYPE"))

        self.__data__.append("END")






    