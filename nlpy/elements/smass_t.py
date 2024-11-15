from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class SMASS_T(Element):
    """
    Элемент заданное граничное условие по расходу
    =====

    Attributes
    ----------
    GIN1 : float
        Заданный расход жидкой фазы (если > 0, расход поступает В ячейку, если < 0, расход поступает Из ячейки) [кг/с]

    GIN2 : float
        Заданный расход газовой фазы (если > 0, расход поступает В ячейку, если < 0, расход поступает Из ячейки) [кг/с]

    GMOUT : float
        Заданный расход смеси, покидающей ячейку [кг/с]
    
    EHIN1 : float
        Энтальпия жидкой фазы, поступающей в соответствии с ключом GIN1, [Дж/кг]

    EHIN2 : float
        Энтальпия газовой фазы, поступающей в соответствии с ключом GIN1, [Дж/кг]

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

        self.__type__ = "SMASS_T"
        self.typepp = self
        self.__name__ = "SMASS_T"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['GIN'][0],
                kwargs['GIN'][1],
                kwargs['GMOUT'],
                kwargs['EHIN'][0],
                kwargs['EHIN'][1]
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.GIN1,
            orig.GIN2,
            orig.GMOUT,
            orig.EHIN1,
            orig.EHIN2
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        GIN1: float,
        GIN2: float,
        GMOUT: float,
        EHIN1: float,
        EHIN2: float,
    ):
        self.GIN1 = np.array(fill_list_or_float(GIN1,1),dtype=float)
        self.GIN2 = np.array(fill_list_or_float(GIN2,1),dtype=float)
        self.GMOUT = np.array(fill_list_or_float(GMOUT,1),dtype=float)
        self.EHIN1 = np.array(fill_list_or_float(EHIN1,1),dtype=float)
        self.EHIN2 = np.array(fill_list_or_float(EHIN2,1),dtype=float)
        self.rebuild()

    def rebuild(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.extend(fill_korsar_array(self.GIN1, "GIN(1)"))
        self.__data__.extend(fill_korsar_array(self.GIN2, "GIN(2)"))
        self.__data__.extend(fill_korsar_array(self.GMOUT, "GMOUT"))
        self.__data__.extend(fill_korsar_array(self.GIN1, "EHIN(1)"))
        self.__data__.extend(fill_korsar_array(self.GIN2, "EHIN(2)"))

        self.__data__.append("END")






    