from database.dbConnection import dbConnection
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

        limit = dbSaveRoute.checkSlotLimit(savedRoutes)
        if (limit <= 9):
            #Update user's save slot with newly created route
            db.child("users").child(uid).child("SavedRoutes").child(routename).update(routeData)
            print("success")
        else:
            print("failed")

    @staticmethod
    def retrieveSaveRoute(self):
        #Open database connection
        firebase = dbConnection.openConn()
        #Access firebase database
        db = firebase.database()

        uid = session['uid']
        savedRoutes = db.child("users").child(uid).child("SavedRoutes").get()

        return savedRoutes


    @staticmethod
    def checkSlotLimit(savedata):
        count =0
        if (savedata.val() is not None):
            for save in savedata.each():
                if (save is not None):
                    count += 1

            return count
        else:
            return 0

