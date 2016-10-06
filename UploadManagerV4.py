import requests
import json

#r = requests.post('http://httpbin.org/post', json={"key": "value"})

url = "http://wheelroutes-humblebees.icitylab.com/rest/coordinate/coordinates"
#data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}

dataCoord = [
  {
     "userId": "9",
     "timestamp": "0",
     "latitude": "0",
	 "numSat":"0",
     "longitude":"0"
     
  }
]

print dataCoord
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(dataCoord), headers=headers)

