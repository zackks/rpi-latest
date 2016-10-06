from ConnectionManager import *
import sqlite3


connGps = OpenGPSConnection()
cursorGps = connGps.execute("SELECT userId, timestamp, latitude, longitude from coordinate")


connAccel = OpenAccelConnection()
cursorAccel = connAccel.execute("SELECT userId, timestamp, xAxis, yAxis, zAxis from accelerometer")

#f = open("testgps2.txt", "a")
#for rowAccel in cursorAccel:
	
	#f.write(str(rowAccel[0]) + ',' + str(rowAccel[1]) + ',' + str(rowAccel[2]) + ',' + str(rowAccel[3]) + ',' + str(rowAccel[4]) + '\n')
	#print "timestamp = " + str(rowAccel[1]) + " ,xAxis = " + str(rowAccel[2]) + " ,yAxis = " + str(rowAccel[3]) + " ,zAxis = " + str(rowAccel[4]) + "\n"
#print "userId = ", rowAccel[0]
#print "timestamp = ", rowAccel[1]
#print "xAxis = ", rowAccel[2]
#print "yAxis = ", rowAccel[3]
#print "zAxis = ", rowAccel[4]

f = open("testgps2.txt", "a")
for rowAccel in cursorGps:
	
	f.write(str(rowAccel[0]) + ',' + str(rowAccel[1]) + ',' + str(rowAccel[2]) + ',' + str(rowAccel[3]) + '\n')


#for rowGps in cursorGps:
#print "userId = ", rowGps[0]
#print "timestamp = ", rowGps[1]
#print "latitude = ", rowGps[2]
#print "longitude = ", rowGps[3]

f.close()
cursorGps.close()
connGps.close()
cursorAccel.close()
connAccel.close()
