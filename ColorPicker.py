#imports OpenCV and Numpy
import cv2
import numpy as np


#creates a "VideoCapture Object"
#0 is the id of the default webcam
capture = cv2.VideoCapture(0)

#sets the size of the frame. 3 for width, 4 for height
capture.set(3, 640)
capture.set(4, 480)
#changes brightness
capture.set(10, 150)

#this function is only used because
#we don't really need a function to run after we change the HSV
def Pass(p):
    pass

#creates a new window named HSV
cv2.namedWindow("HSV")
#resizes the window just to get it out of the way
cv2.resizeWindow("HSV", 640, 240)

#creates sliders to change the individual hue, satruation, and value of an img
cv2.createTrackbar("Hue Min", "HSV", 0, 179, Pass)
cv2.createTrackbar("Sat Min", "HSV", 0, 255, Pass)
cv2.createTrackbar("Val Min", "HSV", 0, 255, Pass)
cv2.createTrackbar("Hue Max", "HSV", 179, 179,Pass)
cv2.createTrackbar("Sat Max", "HSV", 255, 255,Pass)
cv2.createTrackbar("Val Max", "HSV", 255, 255,Pass)



while True:
    _, img = capture.read()
    #converts img into HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #gets the value of HSV from their position on the
    hMin = cv2.getTrackbarPos("Hue Min", "HSV")
    sMin = cv2.getTrackbarPos("Sat Min", "HSV")
    vMin = cv2.getTrackbarPos("Val Min", "HSV")
    hMax = cv2.getTrackbarPos("Hue Max", "HSV")
    sMax = cv2.getTrackbarPos("Sat Max", "HSV")
    vMax = cv2.getTrackbarPos("Val Max", "HSV")

    print('hMin = {} , sMin = {} , vMin = {}'.format(hMin, sMin, vMin))
    print('hMax = {} , sMax = {} , vMax = {}'.format(hMax, sMax, vMax))
    print()

    #arrays to store the lower and upper bounds for the HSV values
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    #creates the mask with the arrays
    mask = cv2.inRange(imgHSV, lower, upper)


    #we can basically merge the mask and the original image
    #this way when we view the picture, only the color we isolated will be there
    #bitwise_and adds two images together to make a new image.
    #bitwise looks at the pixels in both images and if it detects the same pixel it will return a 1 and store it ina  new image
    #bitwise_and(og_img, new_img, mask applied)
    imgResults = cv2.bitwise_and(img, img, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResults)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

