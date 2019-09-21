# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
import os
from distutils.sysconfig import get_python_lib



def trainFaces():
    print("\n [INFO] Training faces. It will take a few seconds. Wait …")
    recogniser = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(get_python_lib() + "/cv2/data/haarcascade_frontalface_default.xml")
    path = "./dataset"   
    
    faces, ids = getImagesAndLabels(path, detector)
    recogniser.train(faces, np.array(ids))

    recogniser.write("trainer/trainer.yml")
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    return str(len(np.unique(ids))) + " faces trained. Exiting Program";

def getImagesAndLabels(path,detector):
    
#let's go through the directory and read images within it
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
#go through each image name, read image, detect face and add face to list of faces
    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        print(imagePath + "/" + str(id))
        #under the assumption that there will be only one face, extract the face area
        for (x, y, w, h) in faces:
            x,y,w,h = faces[0]
            face = img_numpy[y:y + h, x:x + w]
            faceSamples.append(face)
            ids.append(id)

    return faceSamples, ids



