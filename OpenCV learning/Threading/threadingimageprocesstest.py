import threading
import cv2
import numpy as np

class video:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.is_threaded = False

    def init_threads(self):
        self.t1 = threading.Thread(target=cv2.bilateralFilter, args=(self.fr1,7,75,75))
        self.t2 = threading.Thread(target=cv2.bilateralFilter, args=(self.fr2,7,75,75))
        self.t3 = threading.Thread(target=cv2.bilateralFilter, args=(self.fr3,7,75,75))
        self.t4 = threading.Thread(target=cv2.bilateralFilter, args=(self.fr4,7,75,75))
        self.threads = []
        self.threads.append(self.t1)
        self.threads.append(self.t2)
        self.threads.append(self.t3)
        self.threads.append(self.t4)
        self.is_threaded = True

    @staticmethod
    def quantize_frame(frame):
        print(frame.shape)
        y_size = frame.shape[0]
        x_size = frame.shape[1]
        #print(frame[0:int(y_size/2),0:int(x_size/2),:])
        f1 = frame[0:int(y_size/2),0:int(x_size/2),:]
        f2 = frame[int(y_size/2):y_size,0:int(x_size/2),:]
        f3 = frame[0:int(y_size/2),int(x_size/2):x_size,:]
        f4 = frame[int(y_size/2):y_size,int(x_size/2):x_size,:]
        return f1, f2, f3, f4

    def main(self):
        while True:
            ret, frame = self.cap.read()
            self.fr1, self.fr2, self.fr3, self.fr4 = video.quantize_frame(frame)
            if self.is_threaded == False:
                self.init_threads()
            #start threads
            for t in self.threads:
                t.start()
                #wait threads
            for t in self.threads:
                t.join()
            

if __name__ == "__main__":
    vid = video()
    vid.main()
