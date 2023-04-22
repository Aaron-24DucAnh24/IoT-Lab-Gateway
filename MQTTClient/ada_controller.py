
import sys
from uart.uart_controller import UartController
from AIHelper.ai_helper import AIHelper

AIO_FEED_IDs = ['button1', 'button2', 'button3', 'frequency', 'uart_frequency']
READ_SERIAL_FREQUENCY = 0.5

class AdaController:

    ada_frequency   = 0
    confirm_connection_frequency = 10  #const
    auto_mode = 0
    fre_ai = ""

    @staticmethod
    def connect(client):
        print("=> Connected to server")
        for feed in AIO_FEED_IDs:
            client.subscribe(feed)
            client.publish(feed + '/get')

    @staticmethod
    def subscribe(client , userdata , mid , granted_qos):
        print("=> Subscribed to a feed")

    @classmethod
    def message(cls, client , feed_id , payload):
        print("=> Received data " + feed_id + ": " + payload)
        
        if feed_id == 'frequency':
            cls.set_frequency(payload)

        elif feed_id == 'uart_frequency':
            UartController.set_uart_frequency(payload)

        else: 
            cls.handle_control_device(client, feed_id, payload)

    @classmethod
    def set_frequency(cls, payload):
        cls.ada_frequency = int(payload)

    @classmethod
    def publish_data(cls, client, count):
        if count == cls.ada_frequency and UartController.yolobit_connection:
            humidity, temperature, light = UartController.get_uart_data()
            client.publish("sensor1", humidity)
            client.publish("sensor2", temperature)
            client.publish("sensor3", light)
            cls.publish_ai(client)
            print("=> Updating sensors data to MQTT server")

    @classmethod
    def confirm_connection(cls, client, count):
        if count==cls.confirm_connection_frequency:
            client.publish('connection', 'OKAY' if UartController.yolobit_connection else 'No connection to yolobit')
            return True
        return False

    @classmethod
    def update_ada_count(cls, count):
        return count+READ_SERIAL_FREQUENCY if count < cls.ada_frequency else 0

    @classmethod
    def update_confirm_frequency_count(cls, count):
        return count+READ_SERIAL_FREQUENCY if count < cls.confirm_connection_frequency else 0

    @classmethod
    def handle_control_device(cls, client, feed_id, payload):
        if UartController.yolobit_connection:
            UartController.set_btn(feed_id, payload)
            UartController.write_serial(feed_id, str(payload))
            
    @classmethod
    def publish_ai(cls, client):
        ai_result = AIHelper.image_detect()
        if ai_result != cls.fre_ai:
            client.publish('ai', ai_result)
            cls.fre_ai = ai_result
            print('=> Updating AI data to MQTT server')
