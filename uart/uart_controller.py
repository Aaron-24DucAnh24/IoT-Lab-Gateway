
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

    light_btn = ""
    pump_btn = ""
    fan_btn = ""

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
                cls.handle_serial_data(client)
            else:
                cls.handle_disconnection(client, 'fail')
        else:
            cls.handle_disconnection(client, 'fail')
            
    @classmethod
    def handle_disconnection(cls, client, message):
        global disconnect_count
        if message == 'fail':
            disconnect_count += 0.5
            if disconnect_count > cls.uart_frequency:
                cls.yolobit_connection = 0
                disconnect_count = 0
                print('=> No connection to yolobit')
                client.publish('button1', '0')
                client.publish('button2', '0')
                client.publish('button2', '0')
                client.publish('connection', 'No connection to yolobit')
        else:
            disconnect_count = 0
            cls.yolobit_connection = 1
            client.publish('connection', 'OKAY')

    @classmethod
    def write_serial(cls, id, value):
        message = value
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
        return count+0.5 if count < cls.uart_frequency else 0

    @classmethod
    def set_data(cls, client):
        data_list = cls.mess.split('//') if cls.mess else []

        if len(data_list) == 3:
            cls.humidity    = int(data_list[0])
            cls.temperature = int(data_list[1])
            cls.light       = int(data_list[2])
            print('=> Get data from sensor: ', data_list)
            cls.handle_disconnection(client, 'ok')
        else:
            cls.handle_disconnection(client, 'fail')

    @classmethod
    def get_uart_data(cls):
        return cls.humidity, cls.temperature, cls.light

    @classmethod
    def handle_serial_data(cls, client):
        if len(cls.mess) == 2:
            cls.handle_btn_feedback(client)
        else:
            cls.set_data(client)

    @classmethod
    def handle_btn_feedback(cls, client):
        value = mess[-1]
        if mess[0] == 'p' and cls.pump_btn != value:
            client.publish('button1', value)
        elif mess[0] == 'f' and cls.fan_btn != value:
            client.publish('button2', value)
        elif mess[0] == 'l' and cls.light_btn != value:
            client.publish('button3', value)

    @classmethod
    def set_btn(cls, feed_id, payload):
        if feed_id == "button1":
            cls.pump_btn = str(payload)
        elif feed_id == "button2":
            cls.fan_btn = str(payload)
        else:
            cls.light_btn = str(payload)
