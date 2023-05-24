## Roles
1. Get serial data from yolobit, publish to MQTT server
2. Receive control signal from MQTT dashboard and mobile application
3. Use AI module (image detector) to detect if user is wearing mask or not
4. Notify user the status connection to yolobit

## To use

1. Create file ignore.py in ***"/MQTTClient"*** and add MQTT server authentication info
```python
    AIO_USERNAME = '__'
    AIO_KEY      = '__'
```

1. Install dependencies:
```bash
    pip3 install -r requirements.txt
```

2. Test gateway
```bash
    python3 -m unittest test.test_uart -v
    python3 -m unittest test.test_mqtt -v
```

3. Run gateway: 
```bash
    python3 main.py
```
