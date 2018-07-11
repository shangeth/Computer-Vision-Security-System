from flask import Flask, render_template, Response, jsonify, request,redirect,url_for
from camera_recognition import VideoCamera
import cv2
import sqlite3
import os
import numpy as np
from PIL import Image

#flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

video_camera = None
global_frame = None

#Home page for the WebApp
@app.route('/')
def index():
    c = sqlite3.connect("faceInfoData.db")
    conn = c.cursor()
    cur = conn.execute("SELECT * FROM log ")
    logs=cur.fetchall()
    c.commit()
    conn.close()
    return render_template('home.html',logs=logs)

#Record config route
@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

# to stream the video 
def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

#This route shows the video in the html
@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

# page to add new visitors
@app.route('/addVisitor')
def add_visitor():
    return render_template("add_visitor.html")

#page which takes the new visitor details and process it into database
@app.route("/submitVisitor",methods=['POST'])
def submitVisitor():
    if request.method == "POST":

        name = request.form['visitor_name']
        age = request.form['visitor_age']
        sex = request.form['visitor_sex']
        c = sqlite3.connect("faceInfoData.db")
        conn=c.cursor()
        conn.execute("INSERT INTO Visitors (Name, Age, Sex) VALUES (?,?,?)", (name, age, sex))
        c.commit()
        conn.close()
        return render_template("add_face.html",name=name,age=age,sex=sex)

    else:
        return "<h1> Lol ... GET Method not allowed</h1>"


# gets the last id from database to match with the picture takem
def getID():
    conn = sqlite3.connect("faceInfoData.db")
    cur = conn.execute('SELECT max(id) FROM Visitors')
    id = cur.fetchone()[0]
    cur.close()
    return int(id)

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    Ids=[]
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')

        imageNp=np.array(pilImage,'uint8')

        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces=detector.detectMultiScale(imageNp)

        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids



# this page takes pictures for the face recognition
@app.route("/takepic", methods=['GET'])
def takepic():
    cam = cv2.VideoCapture(1)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif idCount > 30:
            break
    cam.release()
    cv2.destroyAllWindows()

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    faces, Ids = getImagesAndLabels('faceData')
    recognizer.train(faces, np.array(Ids))
    print("Training")
    recognizer.save('trainedData/trainingData.yml')
    print("saving to yml")
    return render_template('success.html')


# Shows all the visitors who are allowed
@app.route('/visitorList')
def visitor_list():
    c = sqlite3.connect("faceInfoData.db")
    conn = c.cursor()
    cur = conn.execute("SELECT * FROM Visitors")
    visitors = cur.fetchall()
    return render_template("visitors_list.html",visitors = visitors)



#run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
