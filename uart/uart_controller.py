
import serial.tools.list_ports
import time
import sys

PORT_IDENTIFIER = 'USB Serial' if sys.platform=='darwin' else 'USB-SERIAL'
disconnect_count = 0

class UartController:
    
    # static fields
    ser = None
    mess = ''
    humidity = 0
    temperature = 0
    light = 0
    uart_frequency = 0
    yolobit_connection = 0

    @classmethod
    def set_serial_port(cls):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if PORT_IDENTIFIER in str(port) and not cls.ser:
                cls.ser = serial.Serial(str(port).split(' ')[0], baudrate=115200)

    @classmethod
    def check_serial_port(cls):
        cls.set_serial_port()
        if not cls.ser:
            print('=> No serial port available')
            return False
        return True

    @classmethod
    def read_serial(cls, client):
        if cls.check_serial_port():
            bytesToRead = cls.ser.inWaiting()
            if bytesToRead > 0 :
                cls.mess = cls.ser.read(bytesToRead).decode()
                cls.set_data(client)
            else:
                cls.handle_disconnection(client, 'fail')
        else:
            cls.handle_disconnection(client, 'fail')
            
    @classmethod
    def handle_disconnection(cls, client, message):
        global disconnect_count
        if message == 'fail':
            disconnect_count += 1
            if disconnect_count > cls.uart_frequency:
                cls.yolobit_connection = 0
                disconnect_count = 0
                note = 'No connection to yolobit'
                client.publish('button1', '0')
                client.publish('button2', '0')
                client.publish('button2', '0')
                client.publish('connection', 'No connection to yolobit')
        else:
            disconnect_count = 0
            cls.yolobit_connection = 1
            client.publish('connection', 'OKAY')

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
    def request_data(cls, count):
        if count == cls.uart_frequency and cls.check_serial_port():
            cls.ser.write('get'.encode())

    @classmethod
    def set_uart_frequency(cls, payload):
        cls.uart_frequency = int(payload)

    @classmethod
    def update_uart_count(cls, count):
        return count+1 if count < cls.uart_frequency else 0

    @classmethod
    def set_data(cls, client):
        data_list = cls.mess.split('//') if cls.mess else []

        if len(data_list) == 3:
            cls.humidity    = data_list[0]
            cls.temperature = data_list[1]
            cls.light       = data_list[2]
            print('=> Get data from sensor: ', data_list)
            cls.handle_disconnection(client, 'ok')
        else:
            cls.handle_disconnection(client, 'fail')

    @classmethod
    def get_humidity(cls):
        return cls.humidity

    @classmethod
    def get_temperature(cls):
        return cls.temperature

    @classmethod
    def get_light(cls):
        return cls.light
