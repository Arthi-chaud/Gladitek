from datetime import datetime

class Event:
	def __init__(self, jsonObject):
		self.__raw = jsonObject
		self.__setDate()
		self.title = self.__raw["acti_title"]
		if self.__raw["room"] != None:
			self.room = self.__raw["room"]['code'] if 'room' in self.__raw else None
		
	
	def getUrl(self) -> str:
		year = self.__raw['scolaryear']
		module = self.__raw['codemodule']
		instance = self.__raw['codeinstance']
		activity = self.__raw['codeacti']
		return f"{Intra.URL}/module/{year}/{module}/{instance}/{activity}"

	def __setDate(self) -> None:
		slotKeys = ['rdv_group_registered', 'rdv_indiv_registered']
		gotDate = False
		for slotKey in slotKeys:
			if slotKey in self.__raw:
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
		return any(prof['login'] == intra.email for prof in self.__raw['prof_inst'])