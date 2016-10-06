import sqlite3
import MySQLdb
import psycopg2
import os

#files that are written locally for sensor readings
gpsFileName = 'gpsdData.sqlite'
accelFileName ='accel.sqlite'

#database configurations for mysql
#hostName = "192.168.1.197"
#username = "rpi1"
#dbName = "fyptest"

#database configuration for postgresql (AWS)
#hostName = "humbledb.cst7t5kghsdu.ap-southeast-1.rds.amazonaws.com"
#username = "humble"
#dbName = "humbledb"
#password = "humblebees"
#port = "5432"

#Openshift DB try out
#hostName = "127.5.21.130"
#hostName = "/tmp/"
#username = "admineuhlknj"
#dbName = "wheelroutes"
#username = "kstan.2014@sis.smu.edu.sg"
#password = "qazplm"
#password = "w9JWm7nthIcA"
#port = "5432"

#username = "admindfvpmiy"
#password = "6z12nd-bZ5FY"
#dbName = "pythontest"
#hostName = "127.6.211.2"
#port = "5432"

#AWS wheelroutes
hostName = "dbeeinstance.ct0n0op7km0a.ap-southeast-1.rds.amazonaws.com"
port = "5432"
username = "humble"
password = "humblebees"
dbName = "wheelroutes"

OPENSHIFT_APP_NAME = dbName
OPENSHIFT_POSTGRESQL_DB_USERNAME = username
OPENSHIFT_POSTGRESQL_DB_PASSWORD = password
OPENSHIFT_POSTGRESQL_DB_HOST = hostName
OPENSHIFT_POSTGRESQL_DB_PORT = port

def OpenGPSConnection():
	try:
		
		connGps = sqlite3.connect(gpsFileName)
		print "GPS sqllite connection established."
		return connGps
		
	except Exception, e:
		
		print e
		raise Exception('Failed to establish connection with GPS sqlite.')

def OpenAccelConnection():
	try:
		
		connAccel = sqlite3.connect(accelFileName)
		print 'Accel sqllite connection established.'
		return connAccel
		
	except Exception, e:
		
		print e
		raise Exception('Failed to establish connection with Accel sqlite.')

def OpenDBConnection():
	try:
		
		#connDB = MySQLdb.connect(host=hostName, user=username, db=dbName)
		connDB = psycopg2.connect(host=hostName, user=username, password=password, dbname=dbName, port=port)
		#conn = psycopg2.connect(database=os.environ['OPENSHIFT_APP_NAME'], user=os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'], 
                #password=os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'], host=os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'], 
                #port=os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'] )
		print 'Database connectioned established.'
		return connDB
		
	except Exception, e:
		
		print e
		
	
def CloseConnection(conn):
	try:
		
		conn.close()
	except Exception, e:
		
		print e
		raise Exception('Failed to close connection.')


def SetCursor(conn):
	try:
		
		cursor = conn.cursor()
		return cursor
	except Exception, e:
		
		print e
		raise Exception('Failed to set cursor.')

def CloseCursor(cursor):
	try:
		
		cursor.close()
	except Exception, e:
		
		print e
		raise Exception('Failed to close cursor.')

