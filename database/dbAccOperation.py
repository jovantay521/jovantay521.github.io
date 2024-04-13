from database.dbConnection import dbConnection
from flask import session

class dbAccOp:
    @staticmethod
    def accCreate(userdetails):
        #Grab account information
        #Also, please implement the following error/validation checks
        username = userdetails[0] #Ensure username is more than 6 characters: not implemented
        email = userdetails[1] #Ensure email is valid: not implemented
        pwd = userdetails[2] #Ensure password is more than 6 characters: not implemented

        #Open database connection
        firebase = dbConnection.openConn()
        #Access authentication module and create user account
        auth_Mod = firebase.auth()
        result = auth_Mod.create_user_with_email_and_password(email, pwd)

        if (result != 0):
            #Sign in the user
            result = auth_Mod.sign_in_with_email_and_password(email, pwd)
            #Get the auth user id for creating user's savedata
            user = auth_Mod.get_account_info(result['idToken'])

            #Create a user save data slot in database
            result = dbAccOp.createSaveDataSlot(firebase, username, email, user['users'][0]['localId'])

            return result
        else:
            return 0

    @staticmethod
    def accLogin(userdetails):
        email = userdetails[0]
        pwd = userdetails[1]

        firebase = dbConnection().openConn()
        auth_Mod = firebase.auth()
        result = auth_Mod.sign_in_with_email_and_password(email, pwd)
        if (result != 0):
            return result
        else:
            return 0

    @staticmethod
    def createSaveDataSlot(db_Conn, username, email, uid):
        db = db_Conn.database()
        data = {"Username": username, "Email": email}
        db.child("User_Routes").child(uid).set(data)

    #maybe when logout is coded, can shift the session pop to where it is and remove from here
    @staticmethod
    def accLogout():
        session.pop('username',None)