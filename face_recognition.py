import cv2
import numpy as np
import sqlite3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainedData/trainingData.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

def getProfile(id):
    conn = sqlite3.connect("faceInfoData.db")
    cur = conn.execute("SELECT * FROM People WHERE ID=(?)",(id,))
    profile = None
    for row in cur:
        profile = row
    conn.close()
    return profile



cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        profile = getProfile(Id)
        if (profile != None and conf <50):
            cv2.putText(im,profile[1], (x,y+h),font,1.0, (0,255,0),2)
            cv2.putText(im,str(profile[2]), (x,y+h+30),font,1.0, (0,255,0),2)
            cv2.putText(im,profile[3], (x,y+h+60),font,1.0, (0,255,0),2)
        if conf > 50:
            cv2.putText(im, "Unknown", (x, y + h), font, 1.0, (0, 255, 0),2)
    cv2.imshow('im',im)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
