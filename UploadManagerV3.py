import sqlite3
import MySQLdb
from ConnectionManager import *
from WifiSearch import *
import threading
import urllib2
import json
import requests

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
						  
				userId = str(rowGps[0])
				timestampRaw = str(rowGps[1])
				timestamp = str("" + timestampRaw[:10]) + "T" + str(timestampRaw[11:23]) + "Z" 
				timestampstr = str(timestamp)
				latitude = str(rowGps[2])
				longitude = str(rowGps[3])
				numSat = str(rowGps[4])
				
				print rowGps[0]
				print ""
				print rowGps[2]
				print rowGps[3]
				print rowGps[4]
						  
				dataCoord = dataCoord + [
				  {
					 "userId": userId,
					 "timestamp": timestamp,
					 "latitude": latitude,
					 "numSat": numSat,
					 "longitude":longitude
				  }
				]
				#print 'this is row 0 ---   ', rowGps[0]
				#print 'this is row 1 ---   ', rowGps[1]
				#print 'this is row 2 ---   ', rowGps[2]
				#print 'this is row 3 ---   ', rowGps[3]
				#print 'this is row 4 ---   ', rowGps[4]
				
			#print dataCoord
			
			
			#print json.dumps(dataCoord)
			print 'GPS sqlite data extracted. Attempting to POST GPS data...'
			

			#print dataCoord
			
			#reqGps = urllib2.Request('http://wheelroutes-humblebees.icitylab.com/rest/coordinate/coordinates')
			#reqGps.add_header('Content-Type','application/json')
			#reqGps.add_header('Accept', '*/*')
			
			#responseGps = urllib2.urlopen(reqGps, json.dumps(dataCoord))
			
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			rGps = requests.post('http://wheelroutes.icitylab.com/rest/coordinate/coordinates', data=json.dumps(dataCoord), headers=headers)
			
			dataCoord=[]
			
			print 'Extracting axis sqlite data...'
			
			#for each  accelerometer sensor data entry, break it up and insert into database
			for rowAccel in cursorAccel:
				userId = rowAccel[0]
				timestampRaw = rowAccel[1]
				timestamp = timestampRaw[:10] + 'T' + timestampRaw[10:] + 'Z'
				xAxis = rowAccel[2]
				yAxis = rowAccel[3]
				zAxis = rowAccel[4]
						  
				dataAxis = dataAxis + [
				  {
					 "userId": str(userId),
					 "timestamp": str(timestamp),
					 "xAxis": str(xAxis),
					 "yAxis":str(yAxis),
					 "zAxis": str(zAxis)
				  }
				]

			print dataAxis
			print 'Axis sqlite data extracted, attempting to POST axis data...'
			
			#reqAxis = urllib2.Request('http://wheelroutes-humblebees.rhcloud.com/rest/axis/axes')
			#reqAxis.add_header('Content-Type', 'application/json')
				
			#responseAxis = urllib2.urlopen(reqAxis, json.dumps(dataAxis))
			
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			rAxis = requests.post('http://wheelroutes.icitylab.com/rest/axis/axes', data=json.dumps(dataAxis), headers=headers)
			
			dataAxis = []
			
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
		CREATE TABLE IF NOT EXISTS Coordinate (userId CHAR(2), timestamp CHAR(26), latitude DOUBLE, longitude DOUBLE, numSatellite CHAR(3))''')
		
		cursoraccel.execute('''
		CREATE TABLE IF NOT EXISTS Accelerometer (userId CHAR(2), timestamp CHAR(26), xAxis FLOAT, yAxis FLOAT, zAxis FLOAT)''')
	
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
