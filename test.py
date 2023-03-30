# import serial.tools.list_ports
# import time
# import random

# mess = ''

# ser = serial.Serial('/dev/tty.usbserial-1130', baudrate=115200)

# def readSerial():
#     bytesToRead = ser.inWaiting()
#     if (bytesToRead > 0):
#         global mess
#         mess = ser.read(bytesToRead).decode("UTF-8")
#         print(mess)

# a = ['l1', 'l0', 't1', 't0', 'h1', 'h0']
# count = 0

# while True:

#     if count == 6: count = 0

#     ser.write(a[count].encode())

#     count+=1

#     time.sleep(2)

print('qwerqwr1qwrwqer'.index('1'))
print('asdf'.index('1'))