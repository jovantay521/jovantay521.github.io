from database.dbConnection import dbConnection
from firebase_admin import db
from flask import session

class dbSaveRoute:
    @staticmethod
    def saveRoute(routeData, routename):
        #Open database connection
        firebase = dbConnection.openConn()
        #Access authentication module and create user account
        auth_Mod = firebase.auth()
        #Get the auth user id for creating user's savedata
        token = session['token']
        user = auth_Mod.get_account_info(token)
        uid = user['users'][0]['localId']

        #Access firebase database
        db = firebase.database()
        #Retrieve data to check save slot limit. User can only save 10 routes.
        savedRoutes = db.child("User_Routes").child(uid).child("SavedRoutes")
        limit = dbSaveRoute.checkSlotLimit(savedRoutes)

        if (limit <= 10):
            #Update user's save slot with newly created route
            db.child("User_Routes").child(uid).child("SavedRoutes").child(routename).set(routeData)
            return 1
        else:
            return 0

    @staticmethod
    def checkSlotLimit(data):
        count = 0
        for saveSlot in data:
            count += 1

        return count