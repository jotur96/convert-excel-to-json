from enum import Enum


class Nivel(Enum):
    SIN_NIVEL = 0
    UNO = 1
    DOS = 2
    TRES = 3
    CUATRO = 4

class Parent(Enum):
    NONE = 0
    MAYBE = 1
    IS_PARENT = 2
