from database.dbConnection import dbConnection
from firebase_admin import db
from flask import session

class dbSaveRoute:
    @staticmethod
    def saveRoute(routeData, routename):
        #Open database connection
        firebase = dbConnection.openConn()
        #Access firebase database
        db = firebase.database()

        uid = session['uid']
        #Retrieve data to check save slot limit. User can only save 10 routes.
        savedRoutes = db.child("users").child(uid).child("SavedRoutes").get()

        # limit = dbSaveRoute.checkSlotLimit(savedRoutes)
        # if (limit <= 9):
        #Update user's save slot with newly created route
        db.child("users").child(uid).child("SavedRoutes").child(routename).update(routeData)
        #     return 1
        # else:
        #     return 0

    # @staticmethod
    # def checkSlotLimit(data):
    #     if (data is not None):
    #         print("success")