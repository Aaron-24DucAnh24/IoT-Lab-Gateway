import time
from Adafruit_IO import MQTTClient
from ada_client.ada_controller import *

AIO_USERNAME = 'aaron_24'
AIO_KEY = ''

client = MQTTClient(AIO_USERNAME , AIO_KEY)
print(client)
client.on_connect    = Ada_controller.connect
client.on_disconnect = Ada_controller.disconnected
client.on_message    = Ada_controller.message
client.on_subscribe  = Ada_controller.subscribe
client.connect()
client.loop_background()

def getClient() :
    time.sleep(3)
    return client
