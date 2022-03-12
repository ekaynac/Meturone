import tensorflow as tf
import numpy as np
import cv2 as cv
class letterReader:
    # Image input should be two dimensional: (28,28) or (40,50) etc.
    # Input images should be normalized by ./255
    @staticmethod
    def resizeimg(img, tosize=(32,32)):
        res = cv.resize(img, dsize=tosize)
        res = np.expand_dims(res, -1)
        res = np.expand_dims(res, 0)
        return res
    def __init__(self):
        self.model = tf.keras.models.load_model("letter_recog.model")
        self.alphabet_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    def predict(self, img):
        img_resized = letterReader.resizeimg(img)
        prediction = self.model.predict([img_resized])
        single_letter_prediction = self.alphabet_string[np.argmax(prediction)-1]
        return single_letter_prediction
