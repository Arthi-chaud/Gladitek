from locale import normalize
from os import wait
from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, datetime, timedelta
from sources.Intra import Intra, Event
from gcsa.event import Event as GoogleEvent
from beautiful_date import *

todayFormat = datetime.now().strftime("%Y-%m-%d")

def eventIsKnown(calendar: list, newEvent: Event) -> bool:
	for event in calendar:
		if newEvent.eventCode in event.description:
			return True
	return False

def getCalendarsConf(gladir: str):
	confFilePath = f"{gladir}/gladitek.json"
	confFileContent = open(confFilePath)
	content = json.load(confFileContent)
	return content['calendars'], content['credentials_path']

def getCalendarAPI(gladir: str, credentialPath: str, calendarConf):
	return GoogleCalendar(credentials_path=f"{gladir}/{credentialPath}", token_path=f"{gladir}/{calendarConf['token_path']}", calendar=calendarConf['calendar_id'])

def clearCalendars(gladir: str):
	calendarsConf, credentialPath = getCalendarsConf(gladir)
	today = date.today()
	for calendarConf in calendarsConf:
		calendarAPI = getCalendarAPI(gladir, credentialPath, calendarConf)
		print("Clearing calendar...")
		for event in calendarAPI.get_events((1/Jan/(today.year - 5))[0:00], (1/Jan/(today.year + 5))[0:00]):
			print(f"Removing {event.summary}...")
			calendarAPI.delete_event(event)
		print("Calendar cleared!")

def syncCalendars(gladir: str, fullDump: bool) :
	calendarsConf, credentialPath = getCalendarsConf(gladir)
	today = date.today()
	minDateOnFullDump = (1/Jan/(today.year - 5))[0:00]
	maxDate = (1/Jan/(today.year + 5))[0:00]
	for calendarConf in calendarsConf:
		addedEvents = 0
		calendarAPI = getCalendarAPI(gladir, credentialPath, calendarConf)
		intra = Intra(calendarConf['autologin'])
		newEvents = intra.getAllEvents(minDateOnFullDump if fullDump else date.today())
		oldEvents = [oldEvent for oldEvent in calendarAPI.get_events(time_min=minDateOnFullDump if fullDump else date.today(), time_max=maxDate)]
		for event in newEvents:
			if event.title == None:
				continue
			if not event.isAssignedTo(intra) and not event.isRegisteredTo():
				continue
			if eventIsKnown(oldEvents, event):
				continue
			print(f"Adding {event.title} to calendar")
			addedEvents += 1
			calendarAPI.add_event(GoogleEvent(event.title, start=event.start, end=event.end, description=f"{event.eventCode}\n{event.getUrl()}", location=event.room))
		if addedEvents > 0:
			print(f"Added {addedEvents} events to calendar")
		else:
			print("No event added, up to date!")
