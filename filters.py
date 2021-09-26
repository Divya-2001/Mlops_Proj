import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline

class filters:
    # Normal
    def normal(self, destination):
        img = cv2.imread(destination)
        return img

    # Grey
    def greyscale(self, destination):
        img = cv2.imread(destination)
        greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return greyscale

    # Bright More
    def brightMore(self, destination):
        img = cv2.imread(destination)
        img_bright = cv2.convertScaleAbs(img, beta=80)
        return img_bright

    # Bright Less
    def brightLess(self, destination):
        img = cv2.imread(destination)
        img_bright = cv2.convertScaleAbs(img, beta=-80)
        return img_bright

    # Sharp 
    def sharp(self, destination):
        img = cv2.imread(destination)
        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        img_sharpen = cv2.filter2D(img, -1, kernel)
        return img_sharpen

    # HDR
    def HDREffect(self, destination):
        img = cv2.imread(destination)
        hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
        return  hdr

    # Invert ....
    def invert(self, destination):
        img = cv2.imread(destination)
        inv = cv2.bitwise_not(img)
        return inv

    # LookUpTable ...

    def LookUpTable(self, x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))

    # Summer 
    def summer(self, destination):
        img = cv2.imread(destination)
        increaseLookupTable = self.LookUpTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = self.LookUpTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel  = cv2.split(img)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        sum= cv2.merge((blue_channel, green_channel, red_channel ))
        return sum

    # Winter
    def winter(self, destination):
        img = cv2.imread(destination)
        increaseLookupTable = self.LookUpTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = self.LookUpTable([0, 64, 128, 256], [0, 50, 100, 256])
        blue_channel, green_channel,red_channel = cv2.split(img)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        win= cv2.merge((blue_channel, green_channel, red_channel))
        return win

    def dodgeV2(self,x,y):
        return cv2.divide(x,255-y,scale=256)

    # PencilSketch
    def pencilSketch(self, destination):
        img = cv2.imread(destination)
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(img_gray)
        img_smoothing =cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0)
        finalSketch = self.dodgeV2(img_gray,img_smoothing)
        return finalSketch

