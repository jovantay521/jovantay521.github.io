from dbConnection import dbConnection
from firebase_admin import db


def login(userdetails):
    userdetails[0] = "sgmapgo110"
    userdetails[1] =12345
    dbConn = dbConnection().openConn()

    ref = db.reference("/Users")
    result = ref.get()

    dbConn.closeConn()
