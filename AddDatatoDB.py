import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    # 'storageBucket':"face-612cb.appspot.com"
})

ref =db.reference('User')

data = {
    "CST17IFT00004":
        {
            "name":"Auwal Abdullahi",
            "course":"Info Tech",
            "dept": "Info Tech",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"CST17IFT00017":
        {
            "name":"Nana Asmau Garba",
            "course":"Info Tech",
            "dept": "Info Tech",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"CST17IFT00052":
        {
            "name":"Abdullahi Umar",
            "course":"Info Tech",
            "dept": "Info Tech",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"CST17IFT00055":
        {
            "name":"Adam Yunusa Zakari",
            "course":"Info Tech",
            "dept": "Info Tech",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"CST17IFT00029":
        {
            "name":"Yunus iSA",
            "course":"Info Tech",
            "dept": "Info Tech",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"1319":
        {
            "name":"Yassar Shitu Mukhtar",
            "course":"Computer Sci and Info",
            "dept": "Computer SCi",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"1380":
        {
            "name":"Ahmad Abdulrahman",
            "course":"Software Engineering",
            "dept": "Computer SCi",
            "last_attendace_time":"2022-12-11 11:54:34"

        },
"1403":
        {
            "name":"Mahmud L Yakuku",
            "course":"Software Engineering",
            "dept": "Computer SCi",
            "last_attendace_time":"2022-12-11 11:54:34"

        },

}

for key,value in data.items():
    ref.child(key).set(value)
