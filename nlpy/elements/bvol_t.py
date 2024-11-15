from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class BVOL_T(Element):
    """
    Элемент граничная ячейка с заданным давлением
    =====

    Attributes
    ----------    
    P : numpy.ndarray(dtype=float64)
        Давления в РЯ, [Па]
    
    T1 : numpy.ndarray(dtype=float64)
        Температуры жидкой фазы в РЯ, [К]
    
    T2 : numpy.ndarray(dtype=float64)
        Температуры газовой фазы в РЯ, [К]
    
    VOID : numpy.ndarray(dtype=float64)
        Объемное паросодержание в РЯ, [-]

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

        self.__type__ = "BVOL_T"
        self.typepp = self
        self.__name__ = "BVOL_T"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['P'],
                kwargs['T'][0],
                kwargs['T'][1],
                kwargs['VOID']
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.P,
            orig.T1,
            orig.T2,
            orig.VOID
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        P: Union[float, List[float], np.ndarray],
        T1: Union[float, List[float], np.ndarray],
        T2: Union[float, List[float], np.ndarray],
        VOID: Union[float, List[float], np.ndarray]
    ):
        self.P = np.array(fill_list_or_float(P,1),dtype=float)
        self.T1 = np.array(fill_list_or_float(T1,1),dtype=float)
        self.T2 = np.array(fill_list_or_float(T2,1),dtype=float)
        self.VOID = np.array(fill_list_or_float(VOID,1),dtype=float)
        self.rebuild()

    def rebuild(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.extend(fill_korsar_array(self.P, "P"))
        self.__data__.extend(fill_korsar_array(self.T1, "T(1)"))
        self.__data__.extend(fill_korsar_array(self.T2, "T(2)"))
        self.__data__.extend(fill_korsar_array(self.VOID, "VOID"))

        self.__data__.append("END")






    