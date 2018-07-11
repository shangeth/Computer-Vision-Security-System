import cv2
import sqlite3
import os
import numpy as np
from PIL import Image

'''
To change camera change the 0 to 1 for USB camera.
'''
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def getID():
    conn = sqlite3.connect("faceInfoData.db")
    cur = conn.execute('SELECT max(id) FROM Visitors')
    id = cur.fetchone()[0]
    cur.close()
    return int(id)


id = getID()
idCount = 0
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        idCount = idCount + 1
        cv2.imwrite("faceData/User." + str(id) + '.' + str(idCount) + ".jpg", gray[y:y + h, x:x + w])

        cv2.imshow('frame', img)
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
    elif idCount > 20:
        break
cam.release()
cv2.destroyAllWindows()


recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    Ids=[]

    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')

        imageNp=np.array(pilImage,'uint8')

        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces=detector.detectMultiScale(imageNp)

        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids


faces,Ids = getImagesAndLabels('faceData')
recognizer.train(faces, np.array(Ids))
recognizer.save('trainedData/trainingData.yml')
