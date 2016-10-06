import os
import sys
import time
from gps import *
from datetime import datetime, timedelta

print 'Attempting to access GPS time...'

try:
	gpsd = gps(mode=WATCH_ENABLE)
except:
	print 'No GPS connection present. TIME NOT SET.'
	sys.exit()

while True:
	gpsd.next()
	if gpsd.utc != None and gpsd.utc != '':
		print str(gpsd.utc)
		gpstime = gpsd.utc[0:4] + gpsd.utc[5:7] + gpsd.utc[8:10] + ' ' + gpsd.utc[11:19]
		print str(gpstime)


		print 'Setting system time to GPS time...'
		os.system('sudo date --set="%s"' % gpstime)
		print 'System time set.'
		

		break
		#sys.exit()
		time.sleep(1)
	
currentTime = datetime.now() + timedelta(hours=8)
print currentTime

