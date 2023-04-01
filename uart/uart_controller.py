
import serial.tools.list_ports
import time
import random
from exception.exception import *

def get_serial_port():
    port_name = ''
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'USB Serial' in str(port):
            port_name = str(port).split(' ')[0]
    try:
        serial.Serial(port_name, baudrate=115200)
        return port_name
    except:
        raise InvalidPort(port_name)

port_name = get_serial_port()

class UartController:
    
    # static fields
    ser = serial.Serial(port_name, baudrate=115200)
    mess = ''
    humidity = 0
    temperature = 0
    light = 0
    uart_frequency = 0

    @classmethod
    def read_serial(cls):
        bytesToRead = cls.ser.inWaiting()
        if (bytesToRead > 0):
            cls.mess = cls.ser.read(bytesToRead).decode("UTF-8")
            cls.set_data()
        
    @classmethod
    def write_serial(cls, id, payload):
        message = str(payload)
        if id == 'button1':
            cls.ser.write(('h' + message).encode())
        if id == 'button2':
            cls.ser.write(('t' + message).encode())
        if id == 'button3':
            cls.ser.write(('l' + message).encode())

    @classmethod
    def get_from_sensor(cls, count):
        if count == cls.uart_frequency:
            cls.ser.write('get'.encode())

    @classmethod
    def set_uart_frequency(cls, id, payload):
        if id == 'uart_frequency':
            cls.uart_frequency = int(payload)

    @classmethod
    def update_uart_count(cls, count):
        return count+1 if count < cls.uart_frequency else 0

    @classmethod
    def set_data(cls):
        data_list = []

        # check if mess is available
        if cls.mess: 
            data_list = cls.mess.split('//') 

        if(len(data_list) == 3):
            cls.humidity = data_list[0]
            cls.temperature = data_list[1]
            cls.light = data_list[2]

        print(data_list)

    @classmethod
    def get_humidity(cls):
        return cls.humidity

    @classmethod
    def get_temperature(cls):
        return cls.temperature

    @classmethod
    def get_light(cls):
        return cls.light
