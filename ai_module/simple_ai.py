from keras.models import load_model
import cv2
import numpy as np

np.set_printoptions(suppress=True)
model = load_model("./ai_module/keras_model.h5", compile=False)
class_names = open("./ai_module/labels.txt", "r").readlines()
camera = cv2.VideoCapture(0)
current_ai_data = ''

def ai_detector():
    ret, image = camera.read()
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    return class_name[2:]

def update_ai(client):
    global current_ai_data
    data = ai_detector()
    if data != current_ai_data:
        client.publish("ai", data)
        print("=> Updating ai data: ", data)
    current_ai_data = data
