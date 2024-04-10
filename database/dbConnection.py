# import firebase_admin
# from firebase_admin import credentials
import pyrebase

# This class is used to
class dbConnection:

    def openConn(self):

        config = {
            "apiKey": "AIzaSyBgsLstMsZWuHWnz7SHw9xD41mxjypc7bQ",
            "authDomain": "sgmapgo-b3dc1.firebaseapp.com",
            "databaseURL": "https://sgmapgo-b3dc1-default-rtdb.asia-southeast1.firebasedatabase.app",
            "projectId": "sgmapgo-b3dc1",
            "storageBucket": "sgmapgo-b3dc1.appspot.com",
            "messagingSenderId": "180843502379",
            "appId": "1:180843502379:web:731dc9182fbc86ab1b836e"
        }
        try:
            db_Conn = pyrebase.initialize_app(config)
        except ValueError:
            return 0
        return db_Conn
