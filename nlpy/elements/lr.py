from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class LR(Element):
    """
    Элемент гидравлическое сопротивление
    =====

    Attributes
    ----------
    CSI1 : float
        КГС при прямом направлении потока

    CSI2 : float
        КГС при обратном направлении потока

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

        self.__type__ = "LR"
        self.typepp = self
        self.__name__ = "LR"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['CSI1'],
                kwargs['CSI2']
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.CSI1,
            orig.CSI2
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        CSI1: float,
        CSI2: float
    ):
        self.CSI1 = np.array(fill_list_or_float(CSI1,1),dtype=float)
        self.CSI2 = np.array(fill_list_or_float(CSI2,1),dtype=float)
        self.rebuild_data_block()

    def rebuild_data_block(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.extend(fill_korsar_array(self.BCOND1, "CSI1"))
        self.__data__.extend(fill_korsar_array(self.BCOND2, "CSI2"))

        self.__data__.append("END")






    