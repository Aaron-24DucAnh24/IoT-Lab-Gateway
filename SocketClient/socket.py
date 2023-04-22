
import socketio
from uart.uart_controller import UartController

socket_client = socketio.Client()

socket_client.connect('http://localhost:3000')

@socket_client.on('*')
def catch_message(event, data):
    UartController.write_serial(event, data)
