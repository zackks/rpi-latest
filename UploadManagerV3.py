import sqlite3
import MySQLdb
from ConnectionManager import *
from WifiSearch import *
import threading
import urllib2
import json

def UploadData():
	
	if internet_on():
	
		try:
			print 'Establishing connection...'
			
			#Establish neccessary connections
			connGps = OpenGPSConnection()
			connAccel = OpenAccelConnection()
			#connDB = OpenDBConnection()
			
			print 'All connection established. Setting cursor with given connection...'
			
			#Set cursor with established connection
			cursorGps = SetCursor(connGps)
			cursorAccel = SetCursor(connAccel)
			#cursorDB = SetCursor(connDB)
			
			print 'Cursor set. Reading sensor values stored...'
			
			#extract sensor values using SQL from sqlite
			cursorGps.execute("SELECT userId, timestamp, latitude, longitude, numSatellite from Coordinate")
			cursorAccel.execute("SELECT userId, timestamp, xAxis, yAxis, zAxis from Accelerometer")
			
			print 'Extracting GPS sqlite data...'
			
			#for each  gps sensor data entry, break it up and insert into database
			#for mysql, rmb to unquote table headers and add IGNORE after INSERT
			
			dataCoord = []
			dataAxis =[]
			
			for rowGps in cursorGps:
						  
				userId = rowGps[0]
				timestampRaw = rowGps[1]
				timestampRaw = str(timestampRaw)
				if timestampRaw == "0":
					print timestampRaw
					timestamp= "0"
				else:
					timestamp = timestampRaw[:10] + 'T' + timestampRaw[11:] + 'Z'
				latitude = rowGps[2]
				longitude = rowGps[3]
				numSat = rowGps[4]
						  
				dataCoord = dataCoord + [
				  {
					 "userId": str(userId),
					 "timestamp": str(timestampRaw),
					 "latitude": str(latitude),
					 "longitude":str(longitude),
					 "numSat": str(numSat)
				  }
				]
			
			print dataCoord
			print 'GPS sqlite data extracted. Attempting to POST GPS data...'
			reqCoord = urllib2.Request('http://wheelroutes.icitylab.com/rest/coordinate/coordinates')
			reqCoord.add_header('Content-Type', 'application/json')
			
			responseGPS = urllib2.urlopen(reqCoord,json.dumps(dataCoord))
			
			print 'Extracting axis sqlite data...'
			
			#for each  accelerometer sensor data entry, break it up and insert into database
			for rowAccel in cursorAccel:
				userId = rowAccel[0]
				timestampRaw = rowAccel[1]
				timestampRaw = str(timestampRaw)
				if timestampRaw == "0":
					print timestampRaw
					timestamp= "0"
				else:
					timestamp = timestampRaw[:10] + 'T' + timestampRaw[11:] + 'Z'
				xAxis = rowAccel[2]
				yAxis = rowAccel[3]
				zAxis = rowAccel[4]
						  
				dataAxis = dataAxis + [
				  {
					 "userId": str(userId),
					 "timestamp": str(timestampRaw),
					 "xAxis": str(xAxis),
					 "yAxis":str(yAxis),
					 "zAxis": str(zAxis)
				  }
				]
				
			print 'Axis sqlite data extracted, attempting to POST axis data...'
			
			reqAxis = urllib2.Request('http://wheelroutes.icitylab.com/rest/axis/axes')
			reqAxis.add_header('Content-Type', 'application/json')
				
			responseAxis = urllib2.urlopen(reqAxis, json.dumps(dataAxis))
				
			print "Values uploaded. Attempting to DROP tables..."
			
			DropTables(cursorGps, cursorAccel)
			
			print 'Tables dropped. Recreating empty tables...'
			
			CreateTables(cursorGps, cursorAccel)
			
			print 'Empty tables recreated. Closing all connections and cursors...'
			
			#close all connections to prevent locking the database with multiple access
			CloseCursor(cursorGps)
			CloseConnection(connGps)
			
			CloseCursor(cursorAccel)
			CloseConnection(connAccel)
			
			#CloseCursor(cursorDB)
			#CloseConnection(connDB)

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

if __name__ == "__main__": UploadData()
