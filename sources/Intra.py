import json
import requests
import urllib.parse
from datetime import date, timedelta, datetime

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
	
	def getAllEvents(self, since=date.today()):
		response = self.call('/planning/load', queryParams= {'start': since.strftime("%Y-%m-%d")})
		return [Event(event) for event in response.json()]

class Event:
	def __access(self, obj, field):
		return obj[field] if field in obj else None
	def __init__(self, jsonObject):
		self.__raw = jsonObject
		self.__setDate()
		self.title = self.__access(self.__raw, 'acti_title')
		self.room = None
		if 'room' in self.__raw:
			if self.__raw["room"] != None:
				self.room = self.__access(self.__raw['room'], 'code')
	
	def getUrl(self) -> str:
		year = self.__access(self.__raw, 'scolaryear')
		module = self.__access(self.__raw, 'codemodule')
		instance = self.__access(self.__raw, 'codeinstance')
		activity = self.__access(self.__raw, 'codeacti')
		return f"{Intra.URL}/module/{year}/{module}/{instance}/{activity}"

	def __setDate(self) -> None:
		slotKeys = ['rdv_group_registered', 'rdv_indiv_registered']
		gotDate = False
		for slotKey in slotKeys:
			if slotKey in self.__raw and self.__raw[slotKey] != None:
				slot = self.__raw[slotKey].split('|')
				self.start = self.__datetimeFromStr(slot[0])
				self.end = self.__datetimeFromStr(slot[1])
				gotDate = True
		if not gotDate:
			self.start = self.__datetimeFromStr(self.__raw['start'])
			self.end = self.__datetimeFromStr(self.__raw['end'])
	
	def __datetimeFromStr(self, dateStr) -> datetime:
		return datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
	
	def isRegisteredTo(self):
		return self.__raw['event_registered'] != False

	def isAssignedTo(self, intra) -> bool:
		if 'prof_inst' in self.__raw and self.__raw['prof_inst'] != None:
			return any(prof['login'] == intra.email for prof in self.__raw['prof_inst'])
		return False