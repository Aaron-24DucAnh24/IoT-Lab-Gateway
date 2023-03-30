
import time
from ai_module.simple_ai    import *
from uart.index             import *
from ada_client.declaration import *
from ada_client.method      import *

client = getClient()

sensor_count = 0
uart_count = 0

read_serial()

while True:
    sensor_count     = update_sensor_count(sensor_count)
    uart_count       = update_uart_count(uart_count)

    if uart_count == get_uart_frequency():
        get_from_sensor()

    if sensor_count == get_sensor_frequency():
        update_sensor(client)
        update_ai(client)

    read_serial()

    time.sleep(1)
