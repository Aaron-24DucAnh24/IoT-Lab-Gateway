
import serial.tools.list_ports
import time
import random

ser = serial.Serial('/dev/tty.usbserial-110', baudrate=115200)
mess = ''
humidity = 0
temperature = 0
light = 0
uart_frequency = 0

def read_serial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = ser.read(bytesToRead).decode("UTF-8")
        set_data(mess)

def write_serial(id, payload):
    mess = str(payload)
    if id == 'button1':
        ser.write(('h' + mess).encode())
    if id == 'button2':
        ser.write(('t' + mess).encode())
    if id == 'button3':
        ser.write(('l' + mess).encode())

def get_from_sensor():
    ser.write('get'.encode())

def get_uart_frequency():
    return uart_frequency

def set_uart_frequency(id, payload):
    global uart_frequency
    if id == 'uart_frequency':
        uart_frequency = int(payload)

def update_uart_count(count):
    return count+1 if count < uart_frequency else 0

def set_data(mess:str()):
    data_list = []

    # check if mess is available
    if mess: data_list = mess.split('//') 

    global humidity
    global temperature
    global light

    if(len(data_list) == 3):
        humidity = data_list[0]
        temperature = data_list[1]
        light = data_list[2]
        print(data_list)

def get_humidity():
    return humidity

def get_temperature():
    return temperature

def get_light():
    return light
