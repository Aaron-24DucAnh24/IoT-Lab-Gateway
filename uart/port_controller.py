from exception.exception import NoConnectionPort
import serial.tools.list_ports
import time

class PortController:

    port_name = ''

    @classmethod
    def set_serial_port(cls, port_identifier):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port_identifier in str(port):
                cls.port_name = str(port).split(' ')[0]

    @classmethod
    def check_serial_port(cls):
        if cls.port_name == '':
            print('=> No serial port available')
            return False
        return True

    @classmethod
    def get_serial_port(cls):
        return cls.port_name
