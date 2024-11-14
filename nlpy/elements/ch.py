from ..service import*
from .element import Element
from typing import List
from itertools import count

import numpy as np

class CH(Element):
    """
    Элемент канал
    =====

    Attributes
    ----------
    N : int
        количество РЯ
    
    S : numpy.ndarray
        Площади проходного сечения РЯ, [м2]
    
    PR : numpy.ndarray(dtype=float64)
        Смоченные периметры РЯ, [м]
    
    DZ : numpy.ndarray(dtype=float64)
        Длины РЯ, [м]
    
    DH : numpy.ndarray(dtype=float64)
        Перепады высот РЯ, [м]
    
    P : numpy.ndarray(dtype=float64)
        Давления в РЯ, [Па]
    
    T1 : numpy.ndarray(dtype=float64)
        Температуры жидкой фазы в РЯ, [К]
    
    T2 : numpy.ndarray(dtype=float64)
        Температуры газовой фазы в РЯ, [К]
    
    VOID : numpy.ndarray(dtype=float64)
        Объемное паросодержание в РЯ, [-]
    
    TYPE : numpy.ndarray(dtype=int)
      Тип РЯ
    
    ROU : numpy.ndarray(dtype=float64)
        Шероховатость стенок РЯ, [м]

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

        self.__type__ = "CH"
        self.typepp = self
        self.__name__ = "CH"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['N'],
                kwargs['S'],
                kwargs['PR'],
                kwargs['DZ'],
                kwargs['DH'],
                kwargs['P'],
                kwargs['T'][0],
                kwargs['T'][1],
                kwargs['VOID'],
                kwargs['TYPE'],
                kwargs['ROU']
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.N,
            orig.S,
            orig.PR,
            orig.DZ,
            orig.DH,
            orig.P,
            orig.T1,
            orig.T2,
            orig.VOID,
            orig.TYPE,
            orig.ROU
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        N: int,
        S: Union[float, List[float], np.ndarray],
        PR: Union[float, List[float], np.ndarray],
        DZ: Union[float, List[float], np.ndarray],
        DH: Union[float, List[float], np.ndarray],
        P: Union[float, List[float], np.ndarray],
        T1: Union[float, List[float], np.ndarray],
        T2: Union[float, List[float], np.ndarray],
        VOID: Union[float, List[float], np.ndarray],
        TYPE: Union[int, List[int], np.ndarray],
        ROU: Union[float, List[float], np.ndarray]
    ):
        self.N = N
        self.S = np.array(fill_list_or_float(S,self.N),dtype=float)
        self.PR = np.array(fill_list_or_float(PR,self.N),dtype=float)
        self.DZ = np.array(fill_list_or_float(DZ,self.N),dtype=float)
        self.DH = np.array(fill_list_or_float(DH,self.N),dtype=float)
        self.P = np.array(fill_list_or_float(P,self.N),dtype=float)
        self.T1 = np.array(fill_list_or_float(T1,self.N),dtype=float)
        self.T2 = np.array(fill_list_or_float(T2,self.N),dtype=float)
        self.VOID = np.array(fill_list_or_float(VOID,self.N),dtype=float)
        self.TYPE = np.array(fill_list_or_float(TYPE,self.N),dtype=int)
        self.ROU = np.array(fill_list_or_float(ROU,self.N),dtype=float)

        self.rebuild_data_block()

    def rebuild_data_block(self):
        self.__data__ = []

        self.__data__.append("DATA "+self.__name__)

        self.__data__.append("\tN = "+str(self.N)+";")
        self.__data__.extend(fill_korsar_array(self.S, "S"))
        self.__data__.extend(fill_korsar_array(self.PR, "PR"))
        self.__data__.extend(fill_korsar_array(self.DZ, "DZ"))
        self.__data__.extend(fill_korsar_array(self.DH, "DH"))
        self.__data__.extend(fill_korsar_array(self.P, "P"))
        self.__data__.extend(fill_korsar_array(self.T1, "T(1,1:N)"))
        self.__data__.extend(fill_korsar_array(self.T2, "T(2,1:N)"))
        self.__data__.extend(fill_korsar_array(self.VOID, "VOID"))
        self.__data__.extend(fill_korsar_array(self.TYPE, "TYPE"))
        self.__data__.extend(fill_korsar_array(self.ROU, "ROU"))

        self.__data__.append("END")






    