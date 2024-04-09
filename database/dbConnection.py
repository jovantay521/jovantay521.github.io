import firebase_admin
from firebase_admin import credentials
import os

# Get the user's home directory
home_dir = os.path.expanduser('~')
# Desktop directory path
desktop_dir = os.path.join(home_dir, 'Desktop')

# This class is used to
class dbConnection:
    def openConn(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate(desktop_dir+"\\firebaseToken\\dbCredentials.json")
        # Initialize the app with a service account, granting admin privileges
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://sgmapgo-b3dc1-default-rtdb.asia-southeast1.firebasedatabase.app'
        })
        return default_app

    def closeConn(self,app):
        firebase_admin.delete_app(app)