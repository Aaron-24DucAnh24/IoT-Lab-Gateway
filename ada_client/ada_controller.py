
import sys
from uart.uart_controller import *

AIO_FEED_IDs = ['button1', 'button2', 'button3', 'frequency', 'uart_frequency']

class Ada_controller:

    sensor_frequency = 0

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

        cls.set_frequency(feed_id, payload)

        Uart_controller.write_serial(feed_id, payload)
        Uart_controller.set_uart_frequency(feed_id, payload)

    @classmethod
    def set_frequency(cls, feed_id, payload):
        if feed_id == 'frequency':
            cls.sensor_frequency = int(payload)

    @classmethod
    def get_sensor_frequency(cls):
        return cls.sensor_frequency

    @staticmethod
    def update_sensor(client):
        humidity = Uart_controller.get_humidity()
        temperature = Uart_controller.get_temperature()
        light = Uart_controller.get_light()

        client.publish("sensor1", humidity)
        print("=> Updating humidity: " + str(humidity))

        client.publish("sensor2", temperature)
        print("=> Updating temperature: " + str(temperature))

        client.publish("sensor3", light)
        print("=> Updating light: " + str(light))

    @classmethod
    def update_sensor_count(cls, count):
        return count+1 if count < cls.sensor_frequency else 0
