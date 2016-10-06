from ConnectionManager import *
import sqlite3

connDB = OpenDBConnection()
cursorDB = SetCursor(connDB)

connAccel = OpenAccelConnection()
cursorAccel = connAccel.execute("SELECT userId, timestamp, xAxis, yAxis, zAxis from accelerometer")
		
for rowAccel in cursorAccel:
	cursorDB.execute("""INSERT INTO testaccelerometer
			   ("userId", "timestamp", "xAxis", "yAxis", "zAxis")
			   VALUES (%s, %s, %s, %s, %s)""", (str(rowAccel[0]), str(rowAccel[1]), str(rowAccel[2]), str(rowAccel[3]), str(rowAccel[4])))
	connDB.commit()
	
CloseCursor(cursorDB)
CloseCursor(cursorAccel)
CloseConnection(connAccel)
CloseConnection(connDB)
