#import python libraries
import sys
import os
import time
import threading
from datetime import datetime, timedelta
import sqlite3
import time

#import sensor libraries
from adxl345 import ADXL345
from gps import *

#import self coded python scripts
from UploadManager import *
from ConnectionManager import *
from GitManager import *

sys.path.insert(0, '/home/pi/')
import User
sys.path.insert(0, '/home/pi/rpi-latest')

#initialize necessary global variables
global connGps
connGps = OpenGPSConnection()
cursorGps = SetCursor(connGps)

global connAccel
connAccel = OpenAccelConnection()
cursorAccel = SetCursor(connAccel)

uploading = False

#variables for GPS sensor library
global gpsd
gpsd = None
os.system('sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock') #ensuring gpsd is pointed to the right USB GPS receiver
gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
current_value = None
running = True #setting the thread running to true

adxl345 = ADXL345() #initialize library for accelerometer

# hardcoded userId reflects who is the volunteer, 0 is for administrator
userId = User.id

uploadInterval = 60 #in seconds
frequency = 10 #no of times per while loop for accelerometer

#searches for internet connection & upload data to database in intervals
def OnInterval():
	
	global uploading
	
	threading.Timer(uploadInterval,OnInterval).start()
	try:
		if uploading != True:
		
				uploading = True
				UploadData()
				GitPull()
				
				uploading = False
		
				#connGps = OpenGPSConnection()
				#cursorGps = SetCursor(connGps)
				
				#connAccel = OpenAccelConnection()
				#cursorAccel = SetCursor(connAccel)
		else:
				
				print 'Still uploading...'
	except Exception, e:
		print 'Problem uploading on interval...'
		print e
		uploading = False

#opens and get ready sqlite for writing of sensor values
CreateTables(cursorGps, cursorAccel)

OnInterval()


#main infinite loop
while True:
	
	if gpsd != None and __name__ == '__main__':
		
		#this will continue to loop and grab each set of gpsd info to clear the buffer
		gpsd.next()
		
		try:
		
			#get gps readings
			latitude = gpsd.fix.latitude
			longitude = gpsd.fix.longitude
			utc = gpsd.utc
			time = gpsd.fix.time
			
			gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19] # system time in gps receiver
			
			os.system('sudo date --set="%s"' % gpstime) #sets rpi time with gps system time
			
			if gpsd.utc != None and gpsd.utc != '':
				
				correctedTime = datetime.now() + timedelta(hours=8) #corrected to GMT+8 SGT
			else:
				correctedTime = 0
			#print correctedTime
			
			#print
			#print ' GPS reading'
			#print '----------------------------------------'
			#print 'latitude    ' , latitude
			#print 'longitude   ' , longitude
			#print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
			#print 'altitude (m)' , gpsd.fix.altitude
			#print 'eps         ' , gpsd.fix.eps
			#print 'epx         ' , gpsd.fix.epx
			#print 'epv         ' , gpsd.fix.epv
			#print 'ept         ' , gpsd.fix.ept
			#print 'speed (m/s) ' , gpsd.fix.speed
			#print 'climb       ' , gpsd.fix.climb
			#print 'track       ' , gpsd.fix.track
			#print 'mode        ' , gpsd.fix.mode
			#print
			#print 'sats        ' , gpsd.satellites
			#print ' Satellites (total of', len(gpsd.satellites) , ' in view)'
			
			numSatellites = 0
			
			for i in gpsd.satellites:
				#print '\t', str(i).endswith('y')
				if str(i).endswith('y') == True:
					numSatellites += 1
					
			print numSatellites
			

		except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
			
			print "\nKilling Thread..."
			gpsp.running = False
			gpsp.join() # wait for the thread to finish what it's doing
			print "Done.\nExiting."

		except Exception, e:
			print 'Error handling GPS Receiver.'
			print e
	
		try:
			
			
				
			#latitude = 1.123123
			#longitude = 102.123123
			#record sensor readings only if there is gps fix
			if str(latitude) == 'nan' or latitude == 0.0:
				latitude = 0
				longitude = 0
			
			if uploading == True:
				print 'Upload in progress, no data will be recorded until upload is over to prevent database crash.'
			else:
				
				#print 'timestamp = ' + str(correctedTime) + '   latitude = ' + str(latitude) + '   longitude = ' + str(longitude) + '   numSatellite = ' + str(numSatellites)
				
				cursorGps.execute('''INSERT INTO Coordinate (userId, timestamp, latitude, longitude, numSatellite)
				VALUES ( ?, ?, ?, ?, ? )''', ( buffer(str(userId)),buffer(str(correctedTime)), buffer(str(latitude)), buffer(str(longitude)), buffer(str(numSatellites)) ))
				connGps.commit()
				
				x = 0
				while x < frequency:
					#read accelerometer readings
					axes = adxl345.getAxes(True)
					x += 1
					
					#print "   x = %.3fG" % ( axes['x'] ) + "  y = %.3fG" % (axes['y']) + "  z = %.3fG" % ( axes['z'] )
					
					cursorAccel.execute('''INSERT INTO Accelerometer (userId, timestamp, xAxis, yAxis, zAxis)
					VALUES (?, ?, ?, ?, ?)''', ( buffer(str(userId)), buffer(str(correctedTime)), buffer(str(axes['x'])), buffer(str(axes['y'])), buffer(str(axes['z'])) ) )
					connAccel.commit()
					
					#print "   x = %.3fG" % ( axes['x'] ) + "  y = %.3fG" % (axes['y']) + "  z = %.3fG" % ( axes['z'] )
				x = 0
				
				print 'GPS Receiver and Accelerometer readings has been recorded.'
		
		except Exception, e2:
			
			CreateTables(cursorGps, cursorAccel)
			
			print 'Error handling Accelerometer sensor.'
			print e2
