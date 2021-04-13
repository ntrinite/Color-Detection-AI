#imports OpenCV and Numpy
import cv2
import numpy as np

#creates a "VideoCapture Object"
#0 is the id of the default webcam
capture = cv2.VideoCapture(0)

#sets the size of the frame. 3 for width, 4 for height
capture.set(3, 1280)
capture.set(4, 960)
capture.set(10, 150)

#list to hold the colors we want to detect
#values are recieved from ColorPicker.py
#current first list is a dark blue, second list is green
colors = [[106, 136, 49, 144, 255, 255],
          [46, 43, 43, 92, 255, 255]]

#You know what would be cool? if the color of the markings match the colors of the object
#We can just go ahead and find the rough RGB values of the objects and put them into a list in BGR format
#I could've used the HSV values but just approximating the RGB values was way easier
colorsLookUp = [[245, 85, 70],
                [68, 235, 74]]


#a list that will be used to place the circle at the end of our object
#looks like we're drawing but we're actually just leaving behind a trail of points
#[x, y, colorId]
drawingPoints = []

#used to find all the colors in the image
#whicher ever color is present we want to see it in the output
def FindColor(img, colorList, drawingColor):
    #helps select which color to use
    i= 0

    #Converts the colorspace from Blue Green Red to Hue, Saturation, Value
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    drawPoints = []

    #since we have different colors
    #we're using a loop so it can work for both colors
    for color in colorList:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        #creates a mask that is in range of colors lower and upper
        #we need a range because we know how we can detect the colors we're looking for
        #mask will be a black background and the object with the color will appear white
        #this will be used to find the contours of the object
        mask = cv2.inRange(imgHSV, lower, upper)

        #maskFlip = cv2.flip(mask, 1)
        #cv2.imshow(str(color[0]), maskFlip)

        #recieves the x,y coordinates from GetContours
        x,y = GetContours(mask)

        #draws circle around the point x,y on the bounding box
        #circle(img, coordinates, radius, color, fill_option)
        cv2.circle(imgResults,(x,y), 10,drawingColor[i], cv2.FILLED)

        if x!= 0 and y != 0:
            #We don't need the points if they are 0,0
            #adds the points and the index Id for the drawingColor list (i) to a new list
            #this new list
            drawPoints.append([x,y,i])
        #switches indices which switches colors
        i += 1
    #returns a list that contains an x,y, and what color is selected
    return drawPoints

#used to find contours (points along a boundary)
#this will be useful to find the shape and identify the object that we have defined the colors for
def GetContours(img):
    #the x, y, width, and height value for the contour of the box
    x, y, w ,h = 0, 0, 0, 0

    #findContours(src_img, contour_retrieval_mode, contour_approx)
    #a hiearchy is a relationship of the contours
    #objects can be in different locations and sometimes inside other object.
    #When it is nested the outer one is the parent and the inner one is the child
    #RETR_EXTERNAL retrieves the outermost parent(contours) using this because we only need to find the outer most details
    #CHAIN_APPROX_NONE stores all the contour points, no compression of contour points
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    for cnt in contours:
        # for each contour find the area
        #the area of the contour is the number of pixels inside the contour
        area = cv2.contourArea(cnt)
        print("contour area: {}".format(area))

        #checks for minimum area, like a threshold so it reduces noise
        #if area > pixels
        if area > 500:
            # draws the contours
            # drawContours(src_img, contour, contour_index, color_of_contour, thickness)
            # -1 means that it will draw all the contour
            cv2.drawContours(imgResults, cnt, -1, (0, 0, 0), 2)

            #cv2.arcLength(contour, isClosed)
            perimeter = cv2.arcLength(cnt, True)

            #(from documentation) approximates a curve or a polygon with another curve/polygon with less vertices
            #so that the distance between them is less or equal to the specified precision.
            #using this to try and find corner points of the objects
            #cv2.approxPolyDP(cnt,resolution, isClosed)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

            #takes the approximation of the corners and
            #returns the x, y, width, height
            x, y, w, h = cv2.boundingRect(approx)
    #Don't want to draw from the center of the object but rather the tip
    #floor divde x+ width by 2 to get the center, and we return y to get the tip
    return x+w//2,y

#used to actually "draw' on the image
def Draw(drawPoints, drawColors):
    for point in drawPoints:
        cv2.circle(imgResults,(point[0],point[1]), 10,drawColors[point[2]], cv2.FILLED)



while True:
    #saves the data capqtured into img. Success is a boolean
    success, img = capture.read()

    #This will be the image everything is drawn on
    imgResults = img.copy()
    #imgFlip = cv2.flip(imgResults, 1)

    #finds the color of the object through HSV
    # then returns a list of the coordinates where the circle is and which color is selected
    newDrawPoints = FindColor(img, colors, colorsLookUp)

    #checks to make sure we actually have points
    if len(newDrawPoints) != 0:
        #puts the list from FindColor into drawingPoints as values instead of as a whole list
        for newDP in newDrawPoints:
            drawingPoints.append(newDP)

    if len(drawingPoints) !=0:
        Draw(drawingPoints, colorsLookUp)

    #Displays img
    cv2.imshow("Results", imgResults)
    #adds a delay to the webcam and if the user presses 'q' it'll break out of the loop
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break