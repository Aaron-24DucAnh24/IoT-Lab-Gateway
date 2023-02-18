import sys
from Adafruit_IO import MQTTClient
import time
import random
import simple_ai

AIO_FEED_IDs = ['button1', 'button2']
AIO_USERNAME = 'aaron_24'
AIO_KEY = 'aio_cXKY25YKRkYbb9eYqyKwEb9xgecZ'

def connect(client):
    print("=> Connected to server")
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("=> Subscribed to a feed")

def disconnected(client):
    print("=> Disconnected to server")
    sys.exit (1)

def message(client , feed_id , payload):
    print("=> Received data " + feed_id + ": " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
print(client)
client.on_connect = connect
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

count = 10
ai_count = 5
sensor_type = 0
ai_data = ""
while True:
    count-=1
    if count == 0:
        if sensor_type == 0:
            data = random.randint(15, 60)
            client.publish("sensor1", data)
            print("=> Updating temperature: " + str(data))
            sensor_type = 1
        elif sensor_type == 1:
            data = random.randint(0, 600)
            print("=> Updating light: " + str(data))
            client.publish("sensor2", data)
            sensor_type = 2
        elif sensor_type == 0:
            data = random.randint(0, 100)
            print("=> Updating humidity: " + str(data))
            client.publish("sensor3", data)
            sensor_type = 0
        count = 10

    ai_count -=1
    if ai_count == 0:
        old_ai_data = ai_data
        ai_data = simple_ai.ai_detector()
        if old_ai_data != ai_data:
            client.publish("ai", ai_data)
            print("=> Updating ai data: ", ai_data)
        ai_count = 5

    time.sleep(1)
