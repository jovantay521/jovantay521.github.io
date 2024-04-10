from dbConnection import dbConnection

def accCreate(userdetails):
    username = userdetails[0]
    email = userdetails[1]
    accPassword = userdetails[2]


def accLogin(userdetails):
    userdetails[0] = "sgmapgo110"
    userdetails[1] = 12345

    db_Conn = dbConnection().openConn()


