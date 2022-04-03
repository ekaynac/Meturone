import cv2 as cv
import numpy as np
class Detector:
    @staticmethod
    def nothing(x):
        pass
    @staticmethod
    def drawLine(frame, xs, ys, line_colour = (0,0,255) , line_thickness = 1, font = cv.FONT_HERSHEY_SIMPLEX):
        frame_lined = frame.copy()
        xc = int((xs[0] + xs[1])/2)
        yc = int((ys[0] + ys[1])/2)
        center_x = int(frame_lined.shape[1]/2)
        center_y = int(frame_lined.shape[0]/2)
        center_coordinate = (center_x, center_y)
        obj_center_coordinate = (xc, yc)
        line_lenght = ((xc -center_x)**2 + (yc -center_y)**2)**(1/2)
        cv.line(frame_lined, center_coordinate, obj_center_coordinate, line_colour, line_thickness)
        cv.putText(frame_lined,"Len: {:.2f}".format(line_lenght), (xc,yc), font,
                                            1, (0, 0, 255), 2)
        return frame_lined
    @staticmethod
    def findContours(frame,l_bound,u_bound,dilate=True,draw_contours=False,draw_rectangle=True,filter_type="hsv",kernel_size=(5,5)):
        if filter_type == "hsv":
            frame_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
            mask = cv.inRange(frame_hsv,l_bound,u_bound)
            kernel = np.ones(kernel_size, np.uint8)
            frame_contoured = frame.copy()
            if dilate:
                mask_dilated = cv.dilate(mask, kernel, iterations=1)
                contours, _ = cv.findContours(mask_dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            else:
                contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            if draw_contours:
                cv.drawContours(frame_contoured, contours, -1, (255, 0, 0), 2)
            if draw_rectangle:
                for contour in contours:
                    (x, y, w, h) = cv.boundingRect(contour)

                    if cv.contourArea(contour) > 1000:
                        cv.rectangle(frame_contoured, (x, y), (x+w, y+h), (255,0,0), 2)
                        cv.putText(frame_contoured,"Status: {}".format("Detected"), (10,30), cv.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 3)
            return frame_contoured, frame_hsv, mask, (x,x+w), (y,y+h)
        elif filter_type == "bgr":
            frame_bgr = frame.copy()
            mask = cv.inRange(frame_bgr,l_bound,u_bound)
            kernel = np.ones(kernel_size, np.uint8)
            frame_contoured = frame.copy()
            if dilate:
                mask_dilated = cv.dilate(mask, kernel, iterations=1)
                contours, _ = cv.findContours(mask_dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            else:
                contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            if draw_contours:
                cv.drawContours(frame_contoured, contours, -1, (255, 0, 0), 2)
            if draw_rectangle:
                for contour in contours:
                    (x, y, w, h) = cv.boundingRect(contour)

                    if cv.contourArea(contour) > 1000:
                        cv.rectangle(frame_contoured, (x, y), (x+w, y+h), (255,0,0), 2)
                        cv.putText(frame_contoured,"Status: {}".format("Detected"), (10,30), cv.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 3)
            return frame_contoured, frame_bgr, mask, (x,x+w), (y,y+h)
        
        elif filter_type == "gray":
            frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            mask = cv.inRange(frame_gray,l_bound,u_bound)
            kernel = np.ones(kernel_size, np.uint8)
            frame_contoured = frame.copy()
            if dilate:
                mask_dilated = cv.dilate(mask, kernel, iterations=1)
                contours, _ = cv.findContours(mask_dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            else:
                contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            if draw_contours:
                cv.drawContours(frame_contoured, contours, -1, (255, 0, 0), 2)
            if draw_rectangle:
                for contour in contours:
                    (x, y, w, h) = cv.boundingRect(contour)

                    if cv.contourArea(contour) > 1000:
                        cv.rectangle(frame_contoured, (x, y), (x+w, y+h), (255,0,0), 2)
                        cv.putText(frame_contoured,"Status: {}".format("Detected"), (10,30), cv.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 3)
            return frame_contoured, frame_gray, mask, (x,x+w), (y,y+h)

    def __init__(self,vid_name):
        self.vid_name = vid_name
        self.filter_type = "hsv"
    
    
    
    
    
    
    
    
    
    
    
    
    def main_loop(self):
        cap = cv.VideoCapture(self.vid_name)
        while cap.isOpened():
            ret, self.frame1 = cap.read()
            cv.imshow("init",self.frame1)
            if cv.waitKey(40) == 27:
                break
        cv.destroyAllWindows()
        cap.release()
        
    def findBounds(self,filter_type="hsv"):
        cap = cv.VideoCapture(self.vid_name)
        cv.namedWindow("Filter")
        if filter_type == "hsv":
            cv.createTrackbar("L_H","Filter",0,180,self.nothing)
            cv.createTrackbar("U_H","Filter",180,180,self.nothing)

            cv.createTrackbar("L_S","Filter",0,255,self.nothing)
            cv.createTrackbar("U_S","Filter",255,255,self.nothing)

            cv.createTrackbar("L_V","Filter",0,255,self.nothing)
            cv.createTrackbar("U_V","Filter",255,255,self.nothing)

            while(True):
                ret, frame = cap.read()
                if ret:
                    frame_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

                    l_h = cv.getTrackbarPos("L_H","Filter")
                    u_h = cv.getTrackbarPos("U_H","Filter")

                    l_s = cv.getTrackbarPos("L_S","Filter")
                    u_s = cv.getTrackbarPos("U_S","Filter")

                    l_v = cv.getTrackbarPos("L_V","Filter")
                    u_v = cv.getTrackbarPos("U_V","Filter")

                    l_bound_hsv = np.array([l_h,l_s,l_v])
                    u_bound_hsv = np.array([u_h,u_s,u_v])

                    mask = cv.inRange(frame_hsv, l_bound_hsv, u_bound_hsv)

                    cv.imshow("frame_hsv",frame_hsv)
                    cv.imshow("mask",mask)
                    res = cv.bitwise_and(frame_hsv,frame_hsv,mask=mask)
                    cv.imshow("res",res)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)


                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
            return l_bound_hsv, u_bound_hsv


        elif filter_type == "bgr":
            cv.createTrackbar("L_B","Filter",0,255,self.nothing)
            cv.createTrackbar("U_B","Filter",255,255,self.nothing)

            cv.createTrackbar("L_G","Filter",0,255,self.nothing)
            cv.createTrackbar("U_G","Filter",255,255,self.nothing)

            cv.createTrackbar("L_R","Filter",0,255,self.nothing)
            cv.createTrackbar("U_R","Filter",255,255,self.nothing)

            while(True):
                ret, frame = cap.read()
                if ret:

                    l_b = cv.getTrackbarPos("L_B","Filter")
                    u_b = cv.getTrackbarPos("U_B","Filter")

                    l_g = cv.getTrackbarPos("L_G","Filter")
                    u_g = cv.getTrackbarPos("U_G","Filter")

                    l_r = cv.getTrackbarPos("L_R","Filter")
                    u_r = cv.getTrackbarPos("U_R","Filter")

                    l_bound_bgr = np.array([l_b,l_g,l_r])
                    u_bound_bgr = np.array([u_b,u_g,u_r])

                    mask = cv.inRange(frame,l_bound_bgr,u_bound_bgr)
                    cv.imshow("frame",frame)
                    cv.imshow("mask",mask)
                    res = cv.bitwise_and(frame,frame,mask=mask)
                    cv.imshow("res",res)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)

                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
            return l_bound_bgr, u_bound_bgr
            
        elif filter_type == "gray":
            cv.createTrackbar("L_G","Filter",0,255,self.nothing)
            cv.createTrackbar("U_G","Filter",255,255,self.nothing)

            while(True):
                ret, frame = cap.read()
                if ret:
                    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

                    l_bound_gray = cv.getTrackbarPos("L_G","Filter")
                    u_bound_gray = cv.getTrackbarPos("U_G","Filter")

                    l_bound = np.array([l_bound_gray])
                    u_bound = np.array([u_bound_gray])

                    mask = cv.inRange(frame,l_bound,u_bound)
                    cv.imshow("frame",frame)
                    cv.imshow("mask",mask)
                    res = cv.bitwise_and(frame,frame,mask=mask)
                    cv.imshow("res",res)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
            return l_bound_gray, u_bound_gray
        else:
            print("Try proper filter_type")
            
    def findContoursLive(self,dilate=True,l_bound=np.array([0,0,0]),u_bound=np.array([0,0,0]),draw_contours=False,draw_rectangle=True,filter_type="hsv",line=True):
        cap = cv.VideoCapture(self.vid_name)
        if filter_type == "hsv":
            while(True):
                ret, frame = cap.read()
                if ret:
                    frame_contoured, frame_hsv, mask, xs, ys = Detector.findContours(frame, l_bound=l_bound, u_bound=u_bound, filter_type="hsv")
                    if line:
                        frame_contoured_lined = self.drawLine(frame_contoured,xs,ys)
                    cv.imshow("frame_contoured_lined",frame_contoured_lined)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
        elif filter_type == "bgr":
            while(True):
                ret, frame = cap.read()
                if ret:
                    frame_contoured, frame_bgr, mask, xs, ys = Detector.findContours(frame, l_bound=l_bound, u_bound=u_bound, filter_type="bgr")
                    if line:
                        frame_contoured_lined = self.drawLine(frame_contoured,xs,ys)
                    cv.imshow("frame", frame)
                    cv.imshow("mask",mask)
                    cv.imshow("frame_bgr",frame_bgr)
                    cv.imshow("frame_contoured",frame_contoured)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
            
        elif filter_type == "gray":
            while(True):
                ret, frame = cap.read()
                if ret:
                    frame_contoured, frame_gray, mask, xs, ys = Detector.findContours(frame, l_bound=l_bound, u_bound=u_bound, filter_type="gray")
                    if line:
                        frame_contoured_lined = self.drawLine(frame_contoured,xs,ys)
                    cv.imshow("frame", frame)
                    cv.imshow("mask",mask)
                    cv.imshow("frame_gray",frame_gray)
                    cv.imshow("frame_contoured",frame_contoured)
                else:
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                key = cv.waitKey(24)
                if key==27:
                    break
            cap.release()
            cv.destroyAllWindows()
if __name__ == "__main__":
    flag = int(input("Would you like to use trackbars for filtering? (1/0):\n"))
    if flag == 1:  
        blue_detector = Detector("bluedetection.mp4")
        l_bound ,u_bound = blue_detector.findBounds(filter_type="hsv")
        blue_detector.findContoursLive(l_bound=l_bound,u_bound=u_bound,draw_contours=False, filter_type = "hsv")
    elif flag == 0:
        blue_detector = Detector("bluedetection.mp4")    
        l_bound = np.array([73, 142, 160])
        u_bound = np.array([151, 255, 255])
        blue_detector.findContoursLive(l_bound=l_bound,u_bound=u_bound,draw_contours=False, filter_type = "hsv")