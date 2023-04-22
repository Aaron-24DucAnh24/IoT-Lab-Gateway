from keras.models import load_model
import cv2  
import numpy as np
import time
np.set_printoptions(suppress=True)

class AIHelper:
    model = load_model("./AIHelper/keras_model.h5", compile=False)
    camera = cv2.VideoCapture(0)
    class_names = ['Mask on', 'Mask off', 'No body']    

    @classmethod
    def image_detect(cls):
        ret, image = cls.camera.read()
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1
        prediction = cls.model.predict(image)
        index = np.argmax(prediction)
        return cls.class_names[index]
    
