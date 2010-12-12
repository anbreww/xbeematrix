#!/usr/bin/python
# capture data from webcam
import cv

class Webcam():
    
    def __init__(self, device=0):
        self.capture = cv.CreateCameraCapture(device)

    def get_capture(self,flip=None):
        '''acquire image from camera

        set flip = 1 for image to act as mirror. flip = 0 is vertical mirror'''
        img = cv.QueryFrame(self.capture)
        if flip:
            cv.Flip(img,img,flip)
        return img

    def convert(self, img):
        '''resize, convert to monochrome'''
        gray = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        return gray

    def pick_rectangle(self, img, (xsize,ysize), resizefactor=2):
        (origx, origy) = cv.GetSize(img)
        newsize = (origx/resizefactor, origy/resizefactor)
        resized = cv.CreateImage(newsize, 8, 1)
        cv.Resize(img, resized, cv.CV_INTER_LINEAR)

        # Convert to 1-bit
        th_val = 150
        th_max = 255
        th_type = cv.CV_THRESH_BINARY
        cv.Threshold(resized, resized, th_val, th_max, th_type)

        xcenter = origx/float(2*resizefactor)
        ycenter = origy/float(2*resizefactor)
        small = cv.CreateImage((xsize, ysize), 8, 1)
        cv.GetRectSubPix(resized, small, (xcenter, ycenter))

        return small

    def array(self, image, mode='print'): 
        '''return python array for matrix'''
        (xmax, ymax) = cv.GetSize(image)
        lines = []
        for y in range(ymax):
            line = ''
            for x in range(xmax):
                line = line + ('#' if image[y,x] > 128 else ' ')
            lines.append(line) 
        if mode == 'print':
            print(80*'\n')
            for line in lines:
                print line
        else:
            return lines

    def get_array_from_cam(self, flip=0, (xres,yres)=(96,16), resize=4):
        img = self.get_capture(flip)
        img = self.convert(img)
        small = self.pick_rectangle(img, (xres,yres), resize)
        arr = self.array(small, mode='return')
        return arr




if __name__ == '__main__':
    cam = Webcam(0)
    while 1:
        img = cam.get_capture(flip=1)
        img = cam.convert(img)
        small = cam.pick_rectangle(img, (96,16), 4)
        cam.array(small)

