import numpy as np
import cv2
import os
import sys
face_cascade = cv2.CascadeClassifier('C:\\Users\\tusha\\Downloads\\Programs\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('C:\\Users\\tusha\\Downloads\\Programs\\opencv\\sources\\data\\haarcascades\\haarcascade_upperbody.xml')

#eye_cascade = cv2.CascadeClassifier('C:\\Users\\tusha\\Downloads\\Programs\\opencv\\sources\\data\\haarcascades\\haarcascade_eye.xml')
#eye_cascade = cv2.CascadeClassifier('C:\\Users\\h\\Downloads\\WORK\\opencv3.4\\opencv\\build\\etc\\haarcascades\\haarcascade_eye.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# capture frames from a camera
cap = cv2.VideoCapture('/home/tushar/PycharmProjects/EagleEye/1.mp4')
#print os.path.exists('1.mp4')
#print cv2.getBuildInformation()
#print os.path.exists('haarcascade_eye.xml')
#print os.path.dirname(os.path.abspath(__file__))
#print eye_cascade.load('haarcascade_eye.xml')
#cap = cv2.VideoCapture('1.mp4')
#sys.exit(1)
#fgbg = cv2.createBackgroundSubtractorMOG2()
#cap = cv2.VideoCapture(0)
#ret, frame = cap.read()
#cv2.imwrite('background.png', frame)

# loop runs if capturing has been initialized.
#for i in range(0, 9999):
#while(cap.isOpened()):
while(1):
    # reads frames from a camera
    ret, frame = cap.read()
    print "ret is : " + str(ret)
    print "frame is : " + str(frame)

    # convert to gray scale of each frames
    #frame = cv2.resize(frame, (500,500))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image
    try:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    except Exception as e:
        print e
        sys.exit(1)


    for (x, y, w, h) in faces:
        # To draw a rectangle in a face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detects eyes of different sizes in the input image
#        eyes = eye_cascade.detectMultiScale(roi_gray)

        # To draw a rectangle in eyes
#        for (ex, ey, ew, eh) in eyes:
#            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

#    fgmask = fgbg.apply(frame)
#    final = np.absolute(frame - fgmask)
#    original_image = frame
#    gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
#    background_image = cv2.imread('background.png', cv2.IMREAD_COLOR)
#    gray_background = cv2.cvtColor(background_image, cv2.COLOR_BGR2GRAY)
#
#    foreground = np.absolute(gray_original - gray_background)
#    foreground[foreground > 0] = 255
#
#    # Display an image in a window
#    cv2.imshow('EagleEye', foreground)
#
#    # Wait for Esc key to stop
#    k = cv2.waitKey(30) & 0xff
#    if k == 27:
#        break

# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()