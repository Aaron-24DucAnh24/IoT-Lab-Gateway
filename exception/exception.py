
from abc import ABC

class MyException(ABC, Exception):
    pass

class InvalidPort(MyException):
    def __init__(self, str):
        self.message = 'Invalid serial port: ' + str 
