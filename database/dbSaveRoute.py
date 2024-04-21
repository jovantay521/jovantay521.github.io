from database.dbConnection import dbConnection
from flask import session

class dbSaveRoute:
    @staticmethod
    def saveRoute(routeData, routename):
        try:
            #Open database connection
            firebase = dbConnection.openConn()
            #Access firebase database
            db = firebase.database()

            uid = session['uid']
            #Retrieve data to check save slot limit. User can only save 10 routes.
            savedRoutes = db.child("users").child(uid).child("SavedRoutes").get()

            limit = dbSaveRoute.checkSlotLimit(savedRoutes)
            if (limit < 9):
                duplicateName = dbSaveRoute.checkSameName(savedRoutes, routename)
                if (duplicateName is False):
                    #Update user's save slot with newly created route
                    db.child("users").child(uid).child("SavedRoutes").child(routename).update(routeData)
                    return 1
                else:
                    return 2 #duplicate route name found
            else:
                return 3 #save slot limit reached
        except:
            return 0 #error with firebase

    @staticmethod
    def retrieveSaveRoute():
        try:
            #Open database connection
            firebase = dbConnection.openConn()
            #Access firebase database
            db = firebase.database()
            uid = session['uid']
            savedRoutes = db.child("users").child(uid).child("SavedRoutes").get()
            return savedRoutes
        except:
            return None


    @staticmethod
    def deleteSaveRotue(routeName):
        try:
            #Open database connection
            firebase = dbConnection.openConn()
            #Access firebase database
            db = firebase.database()
            uid = session['uid']

            deletedRoute = db.child("users").child(uid).child("SavedRoutes").child(routeName).remove()
            if deletedRoute.val() is not None:
                return 1
        except:
            return 0

    @staticmethod
    def checkSameName(savedata, routeName):
        if (savedata.val() is not None):
            for save in savedata.each():
                if(save.key() == routeName):
                    return True
        else:
            return False

    @staticmethod
    def checkSlotLimit(savedata):
        count = 0
        if (savedata.val() is not None):
            for save in savedata.each():
                if (save is not None):
                    count += 1

            return count
        else:
            return 0