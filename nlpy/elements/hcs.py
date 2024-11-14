from ..service import*
from .element import Element
from ..materials.material import Material

from typing import List
from itertools import count
import numpy as np

class HCS(Element):
    """
    Элемент канал
    =====

    Attributes
    ----------
    N : int
        количество РЯ


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

        self.__type__ = "HCS"
        self.typepp = self
        self.__name__ = "HCS"+str(self.id)
        self.__model_name__ = model_name

        if orig is None:
            self.__constructor__(
                kwargs['N'],
                kwargs['KL'],
                kwargs['K'],
                kwargs['TYPE'],
                kwargs['COOR'],
                kwargs['XL'],
                kwargs['X'],
                kwargs['MAT'],
                kwargs['DFZ'],
                kwargs['B'],
                kwargs['NGE'],
                kwargs['KIND']
            )
        else:
            self.__copy_constructor__(orig)
        

    def __copy_constructor__(self, orig):
        self.__constructor__(
            orig.N,
            orig.KL,
            orig.K,
            orig.TYPE,
            orig.COOR,
            orig.XL,
            orig.X,
            orig.MAT,
            orig.DFZ,
            orig.B,
            orig.NGE,
            orig.KIND
        )

        # self.__data__ = orig.__data__
        self.__model_name__ = orig.__model_name__

    def __constructor__(
        self,
        N: int,
        KL: int,
        K: int,
        TYPE: int,
        COOR: int,
        XL: Union[float, List[float], np.ndarray],
        X: Union[float, List[float], np.ndarray],
        MAT: Union[Material, List[Material]],
        DFZ: Union[float, List[float], np.ndarray],
        B: float,
        NGE: int,
        KIND: np.ndarray
    ):
        self.N = N
        self.KL = KL
        self.K = K
        self.TYPE = TYPE
        self.COOR = COOR
        self.XL = np.array(fill_list_or_float(XL,self.KL+1),dtype=float)
        self.X = np.array(fill_list_or_float(X,self.K),dtype=float)
        self.MAT = MAT
        self.DFZ = np.array(fill_list_or_float(DFZ,self.N),dtype=float)
        self.B = B
        self.NGE = NGE
        self.KIND = KIND
        
        self.rebuild_data_block()

    def rebuild_data_block(self):
        self.__data__ = []
        
        self.__data__.append("DATA "+self.__name__)

        self.__data__.append("\tN = "+str(self.N)+";")
        self.__data__.append("\tKL = "+str(self.KL)+";")
        self.__data__.append("\tK = "+str(self.K)+";")
        self.__data__.append("\tTYPE = "+str(self.TYPE)+";")
        self.__data__.append("\tCOOR = "+str(self.COOR)+";")
        self.__data__.extend(fill_korsar_array(self.XL, "XL","(1:KL+1)"))
        self.__data__.extend(fill_korsar_array(self.X, "X","(1:K)",))

        self.__data__.append("\tTLAM = ")
        [self.__data__.append("\t\t$"+m.tlam+",") for m in self.MAT]
        self.__data__[-1] = "\t\t$"+self.MAT[-1].tlam+";"
        
        self.__data__.append("\tTHC = ")
        [self.__data__.append("\t\t$"+m.thc+",") for m in self.MAT]
        self.__data__[-1] = "\t\t$"+self.MAT[-1].thc+";"
        
        self.__data__.append("\tTRO = ")
        [self.__data__.append("\t\t$"+m.tro+",") for m in self.MAT]
        self.__data__[-1] = "\t\t$"+self.MAT[-1].tro+";"

        self.__data__.extend(fill_korsar_array(self.DFZ, "DFZ"))
        self.__data__.append("\tB = "+str(self.B)+";")
        self.__data__.append("\tNGE = "+str(self.NGE)+";")
        self.__data__.extend(fill_korsar_array(self.KIND, "KIND", ""))

        self.__data__.append("END")






    