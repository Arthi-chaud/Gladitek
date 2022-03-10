import json
import requests
import urllib.parse
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

class Intra:
	URL = 'https://intra.epitech.eu'
	def __init__(self, autologin):
		self.intraUrl = f"{self.URL}/auth-{autologin}"
		self.email = self.getUserMail()
	
	def call(self, route, queryParams={}):
		queryParams['format'] = 'json'
		return requests.get(f"{self.intraUrl}{route}?{urllib.parse.urlencode(queryParams)}", timeout=600)
	
	def getUserMail(self):
		response = self.call('/user')
		return response.json()['login']
	
	def getPlanning(self, since: date):
		today = date.today()
		elapsedMonths = (today.year - since.year) * 12 + (today.month - since.month)
		dateFormat = "%Y-%m-%d"
		if elapsedMonths > 5: ## Avoid timeouts
			events = []
			for i in range(elapsedMonths):
				dateFromFormat = (since + relativedelta(months=+i)).strftime(dateFormat)
				dateToFormat = (since + relativedelta(months=+(i + 1), days= -1)).strftime(dateFormat)
				print(f"Fetching Intra's events from {dateFromFormat} to {dateToFormat}")
				events.extend(self.call('/planning/load', queryParams= {'start': dateFromFormat, 'end': dateToFormat}).json())
			start = (since + relativedelta(months=elapsedMonths)).strftime(dateFormat)
			print(f"Fetching Intra's events since {start}")
			events.extend(self.call('/planning/load', queryParams= {'start': start}).json())
			return events
		else:
			return self.call('/planning/load', queryParams= {'start': since.strftime(dateFormat)}).json()
	
	def getAllEvents(self, since=date.today()):
		response = self.getPlanning(since)
		return [Event(event) for event in response]
	
	def getRegisteredEvents(self, since=date.today()):
		response = self.getPlanning(since)
		events = []
		for event in response:
			if event['event_registered'] != False:
				events.append(Event(event))
		return events

class Event:
	# Access field fomr JSON Object. If it doesn't exists, returns None
	def __access(self, obj, field):
		return obj[field] if field in obj else None
	def __init__(self, jsonObject):
		self.__raw = jsonObject
		self.__setDate()
		self.title = self.__access(self.__raw, 'acti_title')
		self.room = None
		self.description = self.__access(self.__raw, 'description')
		self.eventCode = self.__access(self.__raw, 'codeevent')
		if 'room' in self.__raw:
			if self.__raw["room"] != None:
				self.room = self.__access(self.__raw['room'], 'code')
	
	# Format description of Event for Google's Event
	def formatDescription(self):
		description = f"{self.description}\n" if self.description != None else ""
		return f"{description}{Intra.URL}{self.getUrl()}\n\nEvent code: {self.eventCode}\n"
	# Returns the Intra's path to acces the activity's page
	def getUrl(self) -> str:
		year = self.__access(self.__raw, 'scolaryear')
		module = self.__access(self.__raw, 'codemodule')
		instance = self.__access(self.__raw, 'codeinstance')
		activity = self.__access(self.__raw, 'codeacti')
		return f"/module/{year}/{module}/{instance}/{activity}"
	# Set's the event start/end date, manages slots and full events
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

	def isAssignedTo(self, intra: Intra) -> bool:
		activity_dump = intra.call(self.getUrl()).json()
		if not 'events' in activity_dump:
			return False
		for event in activity_dump['events']:
			for assistant in event['assistants']:
				if assistant['login'] == intra.email:
					return True
		return False