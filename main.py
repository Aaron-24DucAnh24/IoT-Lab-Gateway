
READ_SERIAL_FREQUENCY = 0.5

import time
from uart.uart_controller      import UartController
from MQTTClient.declaration    import getMqttClient
from MQTTClient.ada_controller import AdaController
from SocketClient.socket       import *

client = getMqttClient()

ada_count = 0
uart_count = 0
confirm_count = 0

while True:
    ada_count      = AdaController.update_ada_count(ada_count)
    confirm_count  = AdaController.update_confirm_frequency_count(confirm_count)
    uart_count     = UartController.update_uart_count(uart_count)

    AdaController.confirm_connection(client, confirm_count)    

    UartController.request_data(uart_count)

    UartController.read_serial(client)

    AdaController.publish_data(client, ada_count)

    time.sleep(READ_SERIAL_FREQUENCY)
