from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from aiot_rgbled import RGBLed
from event_manager import *
import sys
import uselect
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20
from aiot_lcd1602 import LCD1602
import time

tiny_rgb = RGBLed(pin14.pin, 4)

event_manager.reset()

def read_terminal_input():
  spoll=uselect.poll()        # Set up an input polling object.
  spoll.register(sys.stdin, uselect.POLLIN)    # Register polling object.

  input = ''
  if spoll.poll(0):
    input = sys.stdin.read(1)

    while spoll.poll(0):
      input = input + sys.stdin.read(1)

  spoll.unregister(sys.stdin)
  return input

aiot_dht20 = DHT20(SoftI2C(scl=Pin(22), sda=Pin(21)))

aiot_lcd1602 = LCD1602()

def on_event_timer_callback_E_f_m_f_l():
  global input2
  input2 = read_terminal_input()
  if len(input2) != 0:
    if input2[0] == 'g':
      print((str(str(str(round(translate((pin0.read_analog()), 0, 4095, 0, 100))) + '//') + str(str(aiot_dht20.dht20_temperature()) + '//')) + str(round(translate((pin1.read_analog()), 0, 4095, 0, 100)))), end =' ')
    if input2[0] == 'h':
      if input2[1] == '1':
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('pump on')
        print('p1', end =' ')
      else:
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('pump off')
        print('p0', end =' ')
    if input2[0] == 'l':
      if input2[1] == '1':
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('light on')
        print('l1', end =' ')
      else:
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('light off')
        print('l0', end =' ')
    if input2[0] == 't':
      if input2[1] == '1':
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('fan on')
        print('f1', end =' ')
      else:
        aiot_lcd1602.clear()
        aiot_lcd1602.move_to(0, 0)
        aiot_lcd1602.putstr('fan off')
        print('f0', end =' ')

event_manager.add_timer_event(500, on_event_timer_callback_E_f_m_f_l)

if True:
  aiot_lcd1602.move_to(0, 0)
  aiot_lcd1602.putstr('IoT start')

while True:
  event_manager.run()
  time.sleep_ms(500)


pin10.write_analog(round(translate(70, 0, 100, 0, 1023)))
pin10.write_analog(round(translate(0, 0, 100, 0, 1023)))

tiny_rgb.show(0, hex_to_rgb('#ffffff'))
tiny_rgb.show(0, hex_to_rgb('#000000'))

pin3.write_analog(round(translate(70, 0, 100, 0, 1023)))
pin3.write_analog(round(translate(0, 0, 100, 0, 1023)))
