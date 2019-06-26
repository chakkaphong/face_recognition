import numpy as np
import cv2 as cv
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
img = cv.imread('IMG/pam_2.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ccount = 0
ecount = 0

xc = [None] * 2
yc = [None] * 2

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
print("------------------------------------------------------------------------------")
print("found: ",len(faces) , " face")
print("------------------------------------------------------------------------------")
if(len(faces) == 0 ):
    print("No face")
if(len(faces) == 1 ):
    print("Ok")
    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
   
        for (ex,ey,ew,eh) in eyes:
            ccount +=1
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
if(len(faces) == 1 ):
    for r in eyes:
        print("position and side of eye : ",ecount+1, eyes[ecount])
        xc[ecount] = eyes[ecount,2]
        yc[ecount] = eyes[ecount,3]
        ecount += 1


print(faces)
print("------------------------------------------------------------------------------")
print(xc)
print(yc)
Centroid_img1_x = int(xc[0] / 2)
Centroid_img1_y = int(yc[0] / 2)

Centroid_img2_x = int(xc[1] / 2)
Centroid_img2_y = int(yc[1] / 2)

print("XY position1: ", Centroid_img1_x, Centroid_img1_y)
print("XY position2: ", Centroid_img2_x, Centroid_img2_y)

eye1_x = faces[0,0] + eyes[0,0] + Centroid_img1_x 
eye1_y = faces[0,1] + eyes[0,1] + Centroid_img1_y

eye2_x = faces[0,0] + eyes[1,0] + Centroid_img2_x 
eye2_y = faces[0,1] + eyes[1,1] + Centroid_img2_y

cv.line(img,(eye1_x, eye1_y),(eye2_x, eye2_y),(255,0,0),2)
cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()