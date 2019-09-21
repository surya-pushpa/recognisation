#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 
#import os
from distutils.sysconfig import get_python_lib

face_detector = cv2.CascadeClassifier(get_python_lib() + "/cv2/data/haarcascade_frontalface_default.xml")
labels = {}

def detectFace(userId, userName, fileName):
    print("Face ");
    
    cam = cv2.VideoCapture(fileName)
    count = 0
    if( not cam.isOpened()):
         print( "Error opening video stream or file")
         return
     
    while(cam.isOpened()):
        ret, img = cam.read()
        if not ret or img is None:
#            print ("\nPlease look into the camera, your face is not visible")
            continue
            
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
#    
        if(len(faces) == 0):
#            print ("\nPlease look into the camera, your face is not visible")
            continue
        
        #under the assumption that there will be only one face, extract the face area
        (x,y,w,h) = faces[0]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1
        
        filePath = "./dataset/" + str(userId) + '.' + str(count) + ".jpg"
        cv2.imwrite(filePath, gray[y:y+h, x:x+w])
        print(filePath)
        labels[userId] = userName
            
        cv2.imshow("image", img)
    
        cv2.waitKey(1)  # Press 'esc' for exiting video
    
        if count >= 30:
            break
        
    
    print("\n Exiting Program and cleanup stuff " + str(count))
    cam.release()
    cv2.destroyAllWindows()
    print( "Face detection completed")