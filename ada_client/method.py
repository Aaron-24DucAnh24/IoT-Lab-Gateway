
import sys
from uart.index import *

AIO_FEED_IDs = ['button1', 'button2', 'button3', 'frequency', 'uart_frequency']

sensor_frequency = 0

def connect(client):
    print("=> Connected to server")
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)
        client.publish(feed+'/get')

def subscribe(client , userdata , mid , granted_qos):
    print("=> Subscribed to a feed")

def disconnected(client):
    sys.exit (1)

def message(client , feed_id , payload):
    print("=> Received data " + feed_id + ": " + payload)
    write_serial(feed_id, payload)
    set_frequency(feed_id, payload)
    set_uart_frequency(feed_id, payload)

def set_frequency(feed_id, payload):
    global sensor_frequency
    if feed_id == 'frequency':
        sensor_frequency = int(payload)

def get_sensor_frequency():
    return sensor_frequency

def update_sensor(client):
    humidity = get_humidity()
    temperature = get_temperature()
    light = get_light()

    client.publish("sensor1", humidity)
    print("=> Updating humidity: " + str(humidity))

    client.publish("sensor2", temperature)
    print("=> Updating temperature: " + str(temperature))

    client.publish("sensor3", light)
    print("=> Updating light: " + str(light))

def update_sensor_count(count):
    return count+1 if count < sensor_frequency else 0
