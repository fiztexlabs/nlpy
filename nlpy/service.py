import numpy as np
import os
from typing import Union, List


def write_data(data: List[str], path: str = ""):
    """
    Записать текстового блока в файл
    
    Arguments
    ----------
    data : List[str]
        Массив строк для записи

    path : str
        Полный путь к файлу зоны задания
    """
    if path == "":
        path = os.path.join("./block.txt")
        
    with open(path,'w') as f:
        for line in data:
            f.write(line+'\n')


def fill_list_or_float(var: Union[float, int, np.ndarray], N: int = None) -> np.ndarray:
    """
    Сгенерировать массив, заполненный заданными значениями var в зависимости от типа переменной var
    
    Arguments
    ----------
    var : float | int | np.ndarray
        Значение переменной. Если var имеет тип float или int, функция вернет массив размерности N, заполненный значениями
        
    Returns
    ----------
    out : np.ndarray
        Выходной массив
    """
    
    out = np.ndarray

    if type(var) == np.ndarray:
        out = var
    if type(var) == float or type(var) == int:
        out = np.array([var for i in range(N)], dtype = type(var))

    return out


def fill_korsar_array(
    var: np.ndarray, 
    var_name: str,
    numel: str = "(1:N)", 
    tab: str = "\t") -> List[str]:
    """
    Преобразовать входной массив var в список строк для kordat
    
    Arguments
    ----------
    var : np.ndarray
        Значения переменной. Если все значения равны, то в kordat будет записана строка ${var_name}={var[0]}. В противом случае будет записан весь массив

    var_name : str
        Имя переменной

    numel : str
        Границы диапазона (например, (1:N))

    tab : str
        Символы отступа, которые вставляются перед значениями
        
    Returns
    ----------
    data : List[str]
        Выходной массив строк
    """

    data = []
    if np.all(var == var[0]):
        data.append(tab+var_name+"="+str(var[0])+";")
    else:
        data.append(tab+var_name+numel+"=")
        for v in var:
            data.append(tab+'\t'+str(v)+",")
        data[-1] = tab+'\t'+str(var[-1])+";"

    return data