from keras.models import load_model
import cv2
import numpy as np

np.set_printoptions(suppress=True)

class Ai_controller:

    # static fields
    model = load_model("./ai_module/keras_model.h5", compile=False)
    class_names = open("./ai_module/labels.txt", "r").readlines()
    camera = cv2.VideoCapture(0)
    current_ai_data = ''

    @classmethod
    def ai_detector(cls):
        ret, image = cls.camera.read()
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1
        prediction = cls.model.predict(image)
        index = np.argmax(prediction)
        class_name = cls.class_names[index]
        return class_name[2:]

    @classmethod
    def update_ai(cls):
        data = ai_detector()
        if data != cls.current_ai_data:
            client.publish("ai", data)
            print("=> Updating ai data: ", data)
        cls.current_ai_data = data
