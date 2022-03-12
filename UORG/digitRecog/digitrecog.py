import tensorflow as tf
import numpy as np
import cv2 as cv
class numReader:
    # Image input should be two dimensional: (28,28) or (40,50) etc.
    # Input images should be normalized by ./255
    @staticmethod
    def resizeimg(img, tosize=(32,32)):
        res = cv.resize(img, dsize=tosize)
        res = np.expand_dims(res, -1)
        res = np.expand_dims(res, 0)
        return res
    def __init__(self):
        self.model = tf.keras.models.load_model("num_recog.model")
    def predict(self, img):
        img_resized = numReader.resizeimg(img)
        prediction = self.model.predict([img_resized])
        single_digit_prediction = np.argmax(prediction)
        return single_digit_prediction
