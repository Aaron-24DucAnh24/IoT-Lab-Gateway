import time
from Adafruit_IO import MQTTClient
from ada_client.method import *

AIO_USERNAME = 'aaron_24'
AIO_KEY = 'aio_WMBh84JgiYgUQTyeRJ4XAeerNIux'

client = MQTTClient(AIO_USERNAME , AIO_KEY)
print(client)
client.on_connect = connect
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getClient() :
    time.sleep(3)
    return client
