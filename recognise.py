# -*- coding: utf-8 -*-
import cv2
from distutils.sysconfig import get_python_lib

knownUser = set()

def getUsersAppeared(labels, fileName):
    message = recogniseFaces(labels, fileName)
    noOfKnownUser = len(knownUser)
    return noOfKnownUser, message
    
def recogniseFaces(labels, fileName):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./trainer/trainer.yml")
    faceCascade = cv2.CascadeClassifier(get_python_lib() + "/cv2/data/haarcascade_frontalface_default.xml")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    id = 0
    
#    names = ['None', 'Pushpa', 'Chandan', 'A', 'B', 'C']
    names = []
    names.append('None')
    names.extend(list(labels.values()))
    print(names);
    
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    
    while (cam.isOpened()):
    
        ret, img = cam.read()        
        if not ret or img is None:
#            print ("\nPlease look into the camera, your face is not visible")
            continue
        
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        #faces detected at each instance
        for (x, y, w, h) in faces:
    
            #draw rectangle on image according to given (x, y) coordinates and 
            #given width and height & color of rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            #print("\n id: " + str(id) + "/" + names[id])
            
            if confidence < 100:
                name = "unknown"
                if(id < len(names)):
                    name = names[id]
                #name  = str(id)
                con = confidence
                confidence = round(confidence, 0)
    
                if name in names and con < 60:
                    cv2.putText(img, 'matched', (x + 5, y + 25), font, 1, (0, 0, 255), 1)
#                   print(datetime.datetime.now().strftime("%H:%M:%S"))
                else:                    
                    cv2.putText(img, 'not matched', (x + 5, y + 25), font, 1, (0, 0, 255), 1)
                    confidence = round(confidence, 0)
    
                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
#                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                
                if name != "unknown":
                    knownUser.add(id)
                    
        cv2.imshow('camera', img)    
        k = cv2.waitKey(1) # Press 'esc' for exiting video
        if k == 27:
            break
    
    print("\n[INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
