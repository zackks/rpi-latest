import urllib
import socket

REMOTE_SERVER = "www.google.com"

scontext = None

#returns boolean on whether there is internet connection to REMOTE_SERVER
def internet_on():
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host,80),2)
		print 'Internet connection found.'
		return True
	except Exception, e:
		print e
		pass
		print 'No internet connection found.'
		return False
