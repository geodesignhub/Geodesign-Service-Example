import requests, json

class GeodesignHubClient():
	'''
	This a a Python client that uses the Geodesign Hub API to make calls
	and return data. It requires the requests package and the json module. 

	'''
	def __init__(self, url, token):
		'''
		Declare your project id, token and the url (optional). 
		'''
		self.token = token
		self.securl = url if url else 'https://www.geodesignhub.com/api/v1/'


	def post_gdservice_JSON(self, geometry, jobid):
		''' Create a requests object with correct headers and creds. '''
		securl = self.securl+ 'gdservices/callback/'
		headers = {'Authorization': 'Token '+ self.token, 'content-type': 'application/json'}
		data = {"geometry": geometry, "jobid": jobid}
		r = requests.post(securl, headers= headers, data = json.dumps(data))
		return r
