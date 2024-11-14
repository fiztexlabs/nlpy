from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class BHEAT(Element):
    """
    Элемент заданное граничное условие по теплообмену
    =====

    Attributes
    ----------
    TYPE : int
        Тип ГУ

    BCOND1 : float
        ГУ 1

    BCOND2 : float
        ГУ 2

    Methods
    ----------
    rebuild_data_block
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

        self.__type__ = "BHEAT"
        self.typepp = self
        self.__name__ = "BHEAT"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['TYPE'],
                kwargs['BCOND'][0],
                kwargs['BCOND'][1]
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.TYPE,
            orig.BCOND1,
            orig.BCOND2
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        TYPE: int,
        BCOND1: float,
        BCOND2: float
    ):
        self.TYPE = np.array(fill_list_or_float(TYPE,1),dtype=int)
        self.BCOND1 = np.array(fill_list_or_float(BCOND1,1),dtype=float)
        self.BCOND2 = np.array(fill_list_or_float(BCOND2,1),dtype=float)
        self.rebuild_data_block()

    def rebuild_data_block(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.extend(fill_korsar_array(self.TYPE, "TYPE"))
        self.__data__.extend(fill_korsar_array(self.BCOND1, "BCOND(1)"))
        self.__data__.extend(fill_korsar_array(self.BCOND2, "BCOND(2)"))

        self.__data__.append("END")






    