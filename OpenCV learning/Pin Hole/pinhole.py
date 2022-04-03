import cv2 as cv

class Distance:
    def __init__(self,height,focal_lenght,src=0):
        self.distance_px=0 # as px
        self.distance=0 # as m
        self.focal_lenght=focal_lenght # as mm
        self.height=height # as m
        self.angle=0 # as degree
        self.width_px=640 # as px
        self.height_px=480 # as px
        self.cap = cv.VideoCapture(src)

    @staticmethod
    def distance_px_from_contours(self,x_min,y_min,x_max,y_max):
        x = (x_min + x_max)/2
        y = (y_min + y_max)/2
        center_x = self.width_px/2
        center_y = self.height_px/2
        distance = ((center_x - x)^2 + (center_y - y)^2)^(1/2)
        return distance , x, y

    def main(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                #find contours
                #find distance_px from center to countour
                #find distance with pinhole
                cv.imshow("sex",frame)
            if cv.waitKey(10) == ord("q"):
                break

if __name__ == "__main__":
    x = Distance(10,10)
    x.main()