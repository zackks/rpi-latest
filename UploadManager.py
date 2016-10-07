import sqlite3
import MySQLdb
from ConnectionManager import *
from WifiSearch import *
import threading

def UploadData():
	
	if internet_on():
	
		try:
			print 'Establishing connection...'
			
			#Establish neccessary connections
			connGps = OpenGPSConnection()
			connAccel = OpenAccelConnection()
			connDB = OpenDBConnection()
			
			print 'All connection established. Setting cursor with given connection...'
			
			#Set cursor with established connection
			cursorGps = SetCursor(connGps)
			cursorAccel = SetCursor(connAccel)
			cursorDB = SetCursor(connDB)
			
			print 'Cursor set. Reading sensor values stored...'
			
			#extract sensor values using SQL from sqlite
			cursorGps.execute("SELECT userId, timestamp, latitude, longitude, numSatellite  from Coordinate")
			cursorAccel.execute("SELECT userId, timestamp, xAxis, yAxis, zAxis from Accelerometer")
			
			print 'Sensor values extracted. Inserting values into database...'
			
			#for each  gps sensor data entry, break it up and insert into database
			#for mysql, rmb to unquote table headers and add IGNORE after INSERT
			for rowGps in cursorGps:
				cursorDB.execute("""INSERT INTO coord2
						  ("userId", "timestamp", "latitude", "longitude", "numSatellite")
						  VALUES (%s,%s,%s,%s,%s)""", (str(rowGps[0]), str(rowGps[1]), str(rowGps[2]), str(rowGps[3]), str(rowGps[4])))
				connDB.commit()
			
			#for each  accelerometer sensor data entry, break it up and insert into database
			for rowAccel in cursorAccel:
				cursorDB.execute("""INSERT INTO axis2
						   ("userId", "timestamp", "xAxis", "yAxis", "zAxis")
						   VALUES (%s, %s, %s, %s, %s)""", (str(rowAccel[0]), str(rowAccel[1]), str(rowAccel[2]), str(rowAccel[3]), str(rowAccel[4])))
				connDB.commit()
			
			print "Values inserted. Attempting to DROP tables..."
			
			DropTables(cursorGps, cursorAccel)
			
			print 'Tables dropped. Recreating empty tables...'
			
			CreateTables(cursorGps, cursorAccel)
			
			print 'Empty tables recreated. Closing all connections and cursors...'
			
			#close all connections to prevent locking the database with multiple access
			CloseCursor(cursorGps)
			CloseConnection(connGps)
			
			CloseCursor(cursorAccel)
			CloseConnection(connAccel)
			
			CloseCursor(cursorDB)
			CloseConnection(connDB)

			print "Connection and cursor closed. Uploading successfully done!"
		
		except Exception, e:
			
			CreateTables(cursorGps, cursorAccel)
			
			print 'Error encountered. Error as follows:'
			print e
			print 'Uploading unsuccessful.'
			raise Exception("Error encountered. Error as follows: ", e)
		
def CreateTables(cursorgps, cursoraccel):
	try:
		
		cursorgps.execute('''
		CREATE TABLE IF NOT EXISTS Coordinate (userId CHAR(2), timestamp TEXT, latitude DOUBLE, longitude DOUBLE, numSatellite CHAR(3))''')
		
		cursoraccel.execute('''
		CREATE TABLE IF NOT EXISTS Accelerometer (userId CHAR(2), timestamp TEXT, xAxis FLOAT, yAxis FLOAT, zAxis FLOAT)''')
	
	except Exception, e:
		print e
		print 'Unable to CREATE empty tables.'
		
def DropTables(cursorGps, cursorAccel):
	try:
		
		cursorGps.execute("DROP TABLE Coordinate")
		cursorAccel.execute("DROP TABLE Accelerometer")
	
	except Exception, e:
		
		print e
		raise Exception('Unable to DROP tables.')
