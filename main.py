
import time
from ai_module.ai_controller   import *
from uart.uart_controller      import *
from ada_client.declaration    import *
from ada_client.ada_controller import *

client = getClient()

sensor_count = 0
uart_count = 0

Uart_controller.read_serial()

while True:
    sensor_count = Ada_controller.update_sensor_count(sensor_count)
    uart_count   = Uart_controller.update_uart_count(uart_count)

    if uart_count == get_uart_frequency():
        Uart_controller.get_from_sensor()

    if sensor_count == get_sensor_frequency():
        Ada_controller.update_sensor(client)
        Ai_controller.update_ai(client)

    Uart_controller.read_serial()

    time.sleep(1)
