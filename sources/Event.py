from datetime import datetime
from Intra import Intra 

class Event:
	def __init__(self, jsonObject):
		self.__raw = jsonObject
		self.__setDate()
		self.title = self.__raw["acti_title"]
		self.room = self.__raw["room"]['code']
		
	
	def getUrl(self):
		year = self.__raw['scolaryear']
		module = self.__raw['codemodule']
		instance = self.__raw['codeinstance']
		activity = self.__raw['codeacti']
		return f"{Intra.URL}/module/{year}/{module}/{instance}/{activity}"

	def __setDate(self):
		slotKey = 'rdv_group_registered'
		if hasattr(self.__raw, slotKey) == False or self.__raw[slotKey] == None:
			slot = self.__raw[slotKey].split('|')
			self.start = self.__datatimeFromStr(slot[0])
			self.end = self.__datatimeFromStr(slot[1])
		else:
			self.start = self.__datatimeFromStr(self.__raw['start'])
			self.end = self.__datatimeFromStr(self.__raw['end'])
	
	def __datatimeFromStr(str):
		return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
	
	def isRegisteredTo(self):
		return self.__raw['event_registered']

	def isAssignedTo(self, intra):
		return any(prof['login'] == intra.email for prof in self.__raw['prof_inst'])