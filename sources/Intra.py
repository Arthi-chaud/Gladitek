import json
import requests
import urllib.parse
from datetime import datetime
from Event import Event

class Intra:
	URL = 'https://intra.epitech.eu'
	def __init__(self, autologin):
		self.intraUrl = f"{self.URL}/auth-{autologin}"
		self.email = self.getUserMail()
	
	def call(self, route, queryParams={}):
		queryParams['format'] = 'json'
		return requests.get(f"{self.intraUrl}{route}?{urllib.parse.urlencode(queryParams)}")
	
	def getUserMail(self):
		response = self.call('/user')
		return response.json()['login']
	
	def getEvents(self, since=datetime.now()):
		response = self.call('/planning/load', queryParams= {'start': since.strftime("%Y-%m-%d")})
		return [Event(event) for event in response.json()]
