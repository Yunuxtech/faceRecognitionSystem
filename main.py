import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("face-612cb-firebase-adminsdk-wz44r-d3a13202fc.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-612cb-default-rtdb.firebaseio.com/",
    'storageBucket':"face-612cb.appspot.com"
})

bucket = storage.bucket()

# opening the open and setting the dimension
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgBackground = cv2.imread('Resources/background.png')

modefolderpath = 'Resources/Modes'
modePathList = os.listdir(modefolderpath)
imgModeList = []

for path in modePathList:
    imgPath = os.path.join(modefolderpath, path)
    imgModeList.append(cv2.imread(imgPath))

# load encoding file

file = open('EncodeFile.p','rb')
encodeListKnownwithIDs = pickle.load(file)
file.close()
encodeListKnown, studentsID = encodeListKnownwithIDs
print(studentsID)
print("Encode File Loaded")

modeType = 0
counter = 0
ids = -1

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDistance", faceDistance)


        matchIndex = np.argmin(faceDistance)
        print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("known face detected")
            # print(studentsID[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            ids = studentsID[matchIndex]
            imgStudents = []

            # print(ids)

            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:
        if counter == 1:
            # images\CST17IFT00004.png
            print(ids)
            uid = ids.split("/")[1].split(".")[0]
            studentInfo = db.reference(f'User/{uid}').get()
            print(studentInfo)

            blob = bucket.get_blob(f'images/{uid}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudents = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

            ref = db.reference(f'User/{uid}')


        cv2.putText(imgBackground, str(uid), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255),1)
        cv2.putText(imgBackground, str(studentInfo['course']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 1)


        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414-w)//2
        margin = 30  # Adjust this value to set the desired margin

        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 50, 50), 1)
        cv2.putText(imgBackground, str(studentInfo['dept']), (808 + offset, 445 + margin), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (50, 50, 50), 1)

        # Resize imgStudents to (216, 216)
        imgStudents_resized = cv2.resize(imgStudents, (216, 216))

        # Assign the resized imgStudents to the imgBackground array slice
        imgBackground[175:175 + 216, 909:909 + 216] = imgStudents_resized

        # imgBackground [175:175+216,909:909+216] = imgStudents

        # counter+=1

    cv2.imshow("Camera", img)
    cv2.imshow("FaceRecSystem", imgBackground)
    cv2.waitKey(1)
