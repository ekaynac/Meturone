import cv2 as cv
import numpy as np
import imutils

class image_editor():
    def __init__(self,img):
        self.img = img
        self.drawing = False # true if mouse is pressed
        self.ix,self.iy = -1,-1
        self.preview = self.img.copy()
        self.sub_image = self.img.copy()
        self.preview_exist=False
        self.selected_count=0
        self.windowname=""
        self.drawing_circle=False
        self.drawing_rectangle=False
        self.radius = 0


    def operations(self,event,x,y,flags,param):
        #on/off drawing mode if ctrl(8)+leftbutton(1) drawing mode is on
        if flags == 10:
            self.drawing = True
            self.drawing_rectangle = True
            self.drawing_circle = False
        elif flags == 9:
            self.drawing = True
            self.drawing_circle = True
            self.drawing_rectangle = False
        else:
            self.drawing = False
        #when left button down set initial coordinates there and resets preview image
        if event == cv.EVENT_RBUTTONDOWN or event == cv.EVENT_LBUTTONDOWN:
                self.ix,self.iy = x,y
        #in drawing mode reset preview image, draw rectangle on it, set preview_exists to true till we finish drawing
        if self.drawing==True:
            if self.drawing_rectangle:
                self.preview = self.img.copy()
                cv.rectangle(self.preview,(self.ix,self.iy),(x,y),(0,255,0),1)
                self.preview_exist = True
            elif self.drawing_circle:
                self.preview = self.img.copy()
                self.radius = int(((x-self.ix)**2 + (self.iy-y)**2)**(1/2))
                cv.circle(self.preview,(self.ix,self.iy),self.radius,(0,255,0),1)
                self.preview_exist = True
        #if finished drawing mode and a preview exists draw that rectangle on original image
        if (event == cv.EVENT_RBUTTONUP or event == cv.EVENT_LBUTTONUP )and self.preview_exist==True and flags==8:
            self.windowname = "selected"+str(self.selected_count)
            #to make rectangles on any direction
            if self.iy<y:
                y1 = self.iy
                y2 = y
            else:
                y1 = y
                y2 = self.iy
            if self.ix<x:
                x1 = self.ix
                x2 = x
            else:
                x1 = x
                x2 = self.ix
            if event == cv.EVENT_RBUTTONUP:
                cv.rectangle(self.img,(self.ix,self.iy),(x,y),(0,0,255),1)
                sub_image = self.img[y1:y2, x1:x2]
                cv.imshow(self.windowname,sub_image)
                save_name = str(self.windowname)+".jpg"
                cv.imwrite(save_name,self.sub_image)
                self.selected_count +=1
                self.drawing_rectangle=False
                self.preview_exist=False
            elif event == cv.EVENT_LBUTTONUP:
                cv.circle(self.img,(self.ix,self.iy),self.radius,(0,0,255),1)
                self.preview_exist=False
                self.drawing_circle=False
        # on double left click put bgr text
        if(event == cv.EVENT_RBUTTONDOWN):
            b= self.img[x,y,0]
            g= self.img[x,y,1]
            r= self.img[x,y,2]
            font= cv.FONT_HERSHEY_SIMPLEX
            bgr_text = str(b) + " ," + str(g) +  " ," + str(r)
            cv.putText(self.img,bgr_text,(x,y),font,0.3,(0,0,255),1)
        if(event == cv.EVENT_LBUTTONDOWN):
            cv.imwrite("saved.jpg",self.img)
        if (flags==33):
            self.img = imutils.rotate(self.img, 90)
    def session(self):
        cv.namedWindow('image')  
        cv.setMouseCallback('image',self.operations)
        while(1):
            if self.drawing == True:
                cv.imshow('image',self.preview)
            else:
                cv.imshow('image',self.img)
            if cv.waitKey(20) & 0xFF == 27:  
                break  
        cv.destroyAllWindows()  

img = np.zeros((512,512,3), np.uint8)
editor = image_editor(img)
editor.session()