
from abc import ABC

class MyException(ABC, Exception):
    pass

class NoConnectionPort(MyException):
    pass
