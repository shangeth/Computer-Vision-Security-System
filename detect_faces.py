import cv2
import sqlite3

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def insertFaceName(Id,name):
    conn = sqlite3.connect("faceInfoData.db")
    cur = conn.execute("SELECT * FROM People WHERE ID="+str(Id))
    recordExists=0
    for row in cur:
        recordExists = 1
    if(recordExists == 1):
        conn.execute("UPDATE People SET NAME = ?  WHERE ID= ? ",(name,Id))
    else:
        conn.execute("INSERT INTO People (ID,Name) VALUES (?,?)",(Id,name))
    conn.commit()
    conn.close()


Id = int(input('Enter the id : '))
Name = str(input('Enter the Name : '))

insertFaceName(Id,Name)
idCount = 0
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        idCount = idCount + 1
        cv2.imwrite("faceData/User." + str(Id) + '.' + str(idCount) + ".jpg", gray[y:y + h, x:x + w])

        cv2.imshow('frame', img)
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
    elif idCount > 20:
        break
cam.release()
cv2.destroyAllWindows()
