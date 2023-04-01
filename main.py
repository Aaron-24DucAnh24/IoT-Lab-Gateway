
import time
from ai_module.ai_controller   import *
from uart.uart_controller      import *
from ada_client.declaration    import *
from ada_client.ada_controller import *

client = getClient()

sensor_count = 0
uart_count = 0

UartController.read_serial()

while True:
    sensor_count = AdaController.update_sensor_count(sensor_count)
    uart_count   = UartController.update_uart_count(uart_count)

    UartController.get_from_sensor(uart_count)

    AdaController.update_sensor(client, sensor_count)
    AiController.update_ai(client, sensor_count)

    UartController.read_serial()

    time.sleep(1)
