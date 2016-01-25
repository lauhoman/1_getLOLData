import sqlite3

def openDB():
    try:
        conn = sqlite3.connect('data/DataBase.db')
        return conn
    except Exception,e:
        print "Error:openDB Fialed:"
        print e
        return None

def closeDB(conn):
    try:
        conn.close()
        return True
    except Exception,e:
        print "Error:closeDB Fialed:"
        print e
        return False


def searchDB(sql):
    try:
        conn=openDB()
        # print "Opened database successfully"
        cursor = conn.execute(sql)
        #closeDB(conn)
        return cursor
    except Exception,e:
        print 'Error:searchDB Failed:'
        print e
        return None

def editDB(sen):
    try:
        conn=openDB()
        sql=[]
        if type(sen)!=list:
            sql.append(sen)
        else:
            sql=sen

        for item in sql:
            conn.execute(item)

        conn.commit()
        closeDB(conn)
    except Exception,e:
        print 'Error:searchDB Failed:'
        print e
        return None
