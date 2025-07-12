import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import cv2
from tensorflow.python.keras.models import load_model
from collections import deque
import numpy as np
import pickle


class VideoCamera(object):

    def __init__(self):

        self.model = load_model("model/activity.model")
        self.lb = pickle.loads(open("model/lb.pickle", "rb").read())

        self.mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
        self.Q = deque(maxlen=128)

        self.video = cv2.VideoCapture("video/office.mp4")

        #self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    def __del__(self):
        self.video.release()


    def get_frame(self):

        success, image = self.video.read()

        output = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224)).astype("float32")
        image -= self.mean

        output = cv2.resize(output, (1920, 1080)).astype("float32")

        preds = self.model.predict(np.expand_dims(image, axis=0))[0]
        self.Q.append(preds)

        results = np.array(self.Q).mean(axis=0)
        i = np.argmax(results)
        label = self.lb.classes_[i]

        self.text = "Activity: {}".format(label)

        ret, jpeg = cv2.imencode('.jpg', output)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
