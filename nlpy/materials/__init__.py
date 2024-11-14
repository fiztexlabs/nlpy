from .material import Material
import numpy as np

"""Свойства стали 08Х18Н10Т"""
Steel08H18N10T = Material(
    "08X18H10T", 
    np.array([10., 100., 200.]), 
    np.array([16., 18., 19.]),
    np.array([465., 465., 465.]),
    np.array([7850., 7850., 7850.]),
)

