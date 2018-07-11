
import cv2
import threading
import sqlite3
from time import gmtime, strftime,localtime
import pathlib
import dropbox
import re
from twilio.rest import Client
import os


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainedData/trainingData.yml')
global log

def getProfile(id):
    conn = sqlite3.connect("faceInfoData.db")
    cur = conn.execute("SELECT * FROM Visitors WHERE ID=(?)",(id,))
    profile = None
    for row in cur:
        profile = row
    conn.close()
    return profile


def dropbox_sms(filename,msg):
    # the source file
  # located in this folder
      # path object, defining the file
    folder = pathlib.Path("MessageLog")  # located in this folder
  # file name
    filepath = folder / filename

    # target location in Dropbox
    target = "/Temp/"  # the target folder
    targetfile = target + filename  # the target path and file name

    # Create a dropbox object using an API v2 key
    d = dropbox.Dropbox('Enter your Key here!!!')
    '''
    CHANGE THE API from your dropbox account  : change inside of d = dropbox.Dropbox('Your KEY here!!!!')

    '''
    # open the file and upload it
    with filepath.open("rb") as f:
        # upload gives you metadata about the file
        # we want to overwite any previous version of the file
        meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))

    # create a shared link
    link = d.sharing_create_shared_link(targetfile)

    # url which can be shared
    url = link.url

    # link which directly downloads by replacing ?dl=0 with ?dl=1
    dl_url = re.sub(r"\?dl\=0", "?dl=1", url)

    # the following line needs your Twilio Account SID and Auth Token
    client = Client("Account SID here!!", "Auth TOken here!!!")
    '''
    CHANGE THE SID AND AUTH TOKEN HERE!!!!!   
        client = Client("YOur SID Here", "your AUTH Token here")

    '''
    # this is the URL to an image file we're going to send in the MMS
    media = dl_url

    # change the "from_" number to your Twilio number and the "to" number
    # to the phone number you signed up for Twilio with, or upgrade your
    # account to send MMS to any phone number that MMS is available
    '''
    type your phone number in to="phone numer here"
    type your twilio phne number  in from="twilio phone number here" 
    '''
    client.api.account.messages.create(to="+917218540834",
                                       from_="+19412412342",
                                       body=msg,
                                       media_url=media)

def visitor_msg(msgcount,frame,visitor_name):
    '''
    change the path into the path of the folder MessageLog
    '''
    path = '/home/shangeth/Desktop/Detect_face_Final_project/MessageLog/'
    filepath = os.path.join(path, str(msgcount) + '.jpg')
    filename = str(msgcount) + '.jpg'
    cv2.imwrite(filepath, frame)
    msgcount += 1
    msg = "Admin Alert: \n" + str(visitor_name) + " has visited the facility, at " + strftime("%Y-%m-%|%H:%M:%S",localtime())
    # dropbox_sms(filename, msg)


'''
change the path into the path of the folder MessageLog
'''
def unknown_msg(msgcount,frame,visitor_name):
    path = '/home/shangeth/Desktop/Detect_face_Final_project/MessageLog/'
    filepath = os.path.join(path, str(msgcount) + '.jpg')
    filename = str(msgcount) + '.jpg'
    cv2.imwrite(filepath, frame)
    msgcount += 1
    msg = "Admin Alert: \n" + str(visitor_name) + " person entered the facility, at " + strftime("%Y-%m-%d|%H:%M:%S",localtime())
    # dropbox_sms(filename, msg)



class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi', fourcc, 20.0, (640, 480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self):
        # Open a camera
        '''
        change camera here
        inside VideCapture() put 1 for usb camera
        '''
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        count=0
        log = []
        msgcount = 0
        if ret:
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            font = cv2.FONT_HERSHEY_SIMPLEX
            prev_profile = None
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                c = sqlite3.connect("faceInfoData.db")
                conn = c.cursor()
                cur = conn.execute("SELECT visitor_name FROM log WHERE id = (SELECT MAX(id) FROM log)")
                name_q = cur.fetchone()
                if name_q != None:
                    name_q = str(name_q[0])
                else:
                    name_q = None
                conn.close()
                c.close()

                cur_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
                if (conf < 70):
                    profile = getProfile(Id)
                    cv2.putText(frame, profile[1], (x, y + h), font, 1.0, (0, 255, 0), 2)
                    cv2.putText(frame, str(profile[2]), (x, y + h + 30), font, 1.0, (0, 255, 0), 2)
                    cv2.putText(frame, profile[3], (x, y + h + 60), font, 1.0, (0, 255, 0), 2)


                    if prev_profile != profile and name_q != profile[1]:
                        log.append([profile,cur_time])
                        c = sqlite3.connect("faceInfoData.db")
                        conn = c.cursor()
                        conn.execute("INSERT INTO log (visitor_name, time) VALUES (?,?)", (profile[1],str(cur_time)))
                        c.commit()
                        conn.close()

                        thread = threading.Thread(target=visitor_msg, args=(msgcount,frame,profile[1]))
                        thread.daemon = True  # Daemonize thread
                        thread.start()  # Start the execution
                        
                        prev_profile = profile



                elif conf >=70 :
                    Id=0
                    profile=None
                    if name_q != 'Unknown':
                        log.append([['Unknown','',''], cur_time])
                        c = sqlite3.connect("faceInfoData.db")
                        conn = c.cursor()
                        conn.execute("INSERT INTO log (visitor_name, time) VALUES (?,?)", ('Unknown', str(cur_time)))
                        c.commit()
                        conn.close()

                        thread = threading.Thread(target=unknown_msg, args=(msgcount, frame, 'Unknown'))
                        thread.daemon = True  # Daemonize thread
                        thread.start()  # Start the execution

                    cv2.putText(frame, "Unknown", (x, y + h), font, 1.0, (0, 255, 0), 2)
                    prev_profile = profile

            count +=1
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()


