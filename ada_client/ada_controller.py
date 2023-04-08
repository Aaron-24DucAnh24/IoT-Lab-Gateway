
import sys
from uart.uart_controller import UartController

AIO_FEED_IDs = ['button1', 'button2', 'button3', 'frequency', 'uart_frequency']

class AdaController:

    ada_frequency   = 0
    pre_humidity    = 0
    pre_light       = 0
    pre_temperature = 0

    @staticmethod
    def connect(client):
        print("=> Connected to server")
        for feed in AIO_FEED_IDs:
            client.subscribe(feed)
            client.publish(feed + '/get')

    @staticmethod
    def subscribe(client , userdata , mid , granted_qos):
        print("=> Subscribed to a feed")

    @staticmethod
    def disconnected(client):
        sys.exit(1)

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
        if count == cls.ada_frequency:
            
            humidity    = UartController.get_humidity()
            temperature = UartController.get_temperature()
            light       = UartController.get_light()

            if humidity != cls.pre_humidity:
                client.publish("sensor1", humidity)
                print("=> Updating humidity: " + str(humidity))

            if temperature != cls.pre_temperature:
                client.publish("sensor2", temperature)
                print("=> Updating temperature: " + str(temperature))

            if light != cls.pre_light:
                client.publish("sensor3", light)
                print("=> Updating light: " + str(light))

            cls.pre_humidity    = humidity
            cls.pre_temperature = temperature
            cls.pre_light       = light

    @classmethod
    def update_ada_count(cls, count):
        return count+1 if count < cls.ada_frequency else 0

    @classmethod
    def handle_control_device(cls, client, feed_id, payload):
        if UartController.yolobit_connection:
            UartController.write_serial(feed_id, payload)
        elif str(payload) == '1':
                client.publish(feed_id, '0')
