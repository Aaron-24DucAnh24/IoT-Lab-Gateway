
import time
from uart.uart_controller      import *
from ada_client.declaration    import *
from ada_client.ada_controller import *

client = getClient()

ada_count = 0
uart_count = 0

while True:
    ada_count  = AdaController.update_ada_count(ada_count)

    uart_count = UartController.update_uart_count(uart_count)

    UartController.request_data(uart_count)

    UartController.read_serial(client)

    AdaController.publish_data(client, ada_count)

    time.sleep(1)
