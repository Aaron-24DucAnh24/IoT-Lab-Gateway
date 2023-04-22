import time
from Adafruit_IO import MQTTClient
from MQTTClient.ada_controller import AdaController

AIO_USERNAME = 'aaron_24'
AIO_KEY = ''

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
