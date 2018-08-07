# Computer-Vision-Security-System
A Security System using the face recognition, which can be monitored from anywhere using a HTTP server, coded using Python and Jinja2.
<br><br>

# Installation
## System Requirements

### 1. Python3
> Install Python3 for Windows/Linux/Mac OS from https://www.python.org/downloads/release/python-3

### 2. SqliteBrowser(for sqlite database)
> Download and Install SQLite Browser , to view/modify the sqlite database from https://sqlitebrowser.org/

### 3. pip
> 1. Download it get-pip.py file from https://bootstrap.pypa.io<br>
> 2. Open terminal and install pip  `python get-pip.py`

<br><br>
## Python Packages Requirements
> `pip install numpy pillow flask opencv-python opencv-contrib-python twilio dropbox`

<br><br>
## Hardware Requirements
> 1. 2 cameras, 1 for surveillance and another to take face data for training face recognizer<br>
> 2. A server to host the Web server <br>
> 3. Router (optional)

<br><br>
## Cloning the code from git
> 1. `git clone https://github.com/shangeth/Computer-Vision-Security-System.git`

<br><br>
## Running the program
> 1. `cd server`
> 2. `python server.py` this will open the webserver on `127.0.0.1:5000`

<br><br>
## How does it work
> 1. Home page will show live feed of camera and log of people who visited the facility.
> 2. Add Visitor allows you to enter the details of new visitor who need to be added/permitted into the facility.
> 3. After adding details of the new visitor, `python detect_faces.py`. Before running it make sure the new visitor’s face is in front of the second USB camera.

<br><br>
## Enabling SMS notification(optional)
> 1. Go to `twilio.com` and create an developer account and get the auth token and SID for the application.
> 2. Go to `dropbox.com` and create an developer account and generate auth token for the application in create app section.
> 3. `nano camera_recognition.py` and edit line 40 and 61 to enter your credentials.
