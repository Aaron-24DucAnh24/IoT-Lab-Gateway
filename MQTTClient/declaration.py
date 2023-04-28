import time
from MQTTClient.ignore import *
from Adafruit_IO import MQTTClient
from MQTTClient.ada_controller import AdaController

client = MQTTClient(AIO_USERNAME , AIO_KEY)
print(client)
client.on_connect    = AdaController.connect
client.on_message    = AdaController.message
client.on_subscribe  = AdaController.subscribe
client.connect()
client.loop_background()

def getMqttClient() :
    time.sleep(3)
    return client
