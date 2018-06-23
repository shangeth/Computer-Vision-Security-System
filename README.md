<h1>Face Recognition </h1>
<p>This is a OpenCV based Face Recognition script which uses haarcascades algorithm for face detection and LBPH for face recognition.</p>
<hr>
<h2>Scripts explaination:</h2>
<ol>
<li>
  <strong>detect_faces.py</strong>
  <br>
  ```
 cam = cv2.VideoCapture(0) is used to initialize and capture the video cam
  
 detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') is the classifier used to detect the face in any image
 
    <p><a href="https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html">Haar Cascade</a> is used for the detection of face in an image or frame of a video</p>
    
 insertFaceName() function connects to the database and search for the given id , updates/or creates a new entry int the database
 
 ret, img = cam.read()   img captures each frame of the video 
 
 cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) changes the image to the gray scale 
 
 faces = detector.detectMultiScale(gray, 1.3, 5) returns the faces object , which has the coordinates for the face
 
 for (x, y, w, h) in faces:<br>
          cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    draws the rectangle with the coordinates in faces

  </li>

```





<li><strong>train_dataset.py</strong></li>
<li><strong>face_recognition.py</strong></li>
</ol>
