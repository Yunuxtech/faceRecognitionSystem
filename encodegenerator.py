import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import storage

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket':"face-612cb.appspot.com"
})
#importing the students images

folderpath = 'images'
PathList = os.listdir(folderpath)
imgList = []

print(PathList)

studentsID = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderpath, path)))
    studentsID.append(os.path.join(folderpath, path))
    # print(os.path.splitext(path[0]))
    # print(len(imgList))
    # print(studentsID)

    filename = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


def findEncodings(imageList):
    encodeList= []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
print(encodeListKnown)
encodeListKnownwithID = [encodeListKnown,studentsID]
print("Encoding Complete")


file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownwithID, file)
file.close()
print("file saved")