from locale import normalize
from os import wait
from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, datetime, timedelta
from sources.Intra import Intra, Event
from gcsa.event import Event as GoogleEvent
from beautiful_date import *

todayFormat = datetime.now().strftime("%Y-%m-%d")

# Check if new event is already in calendar using event's code
def eventIsKnown(calendar: list, newEvent: Event) -> bool:
	for event in calendar:
		if newEvent.eventCode in event.description:
			return True
	return False

# Open and parse gladitek.json
def getCalendarsConf(gladir: str):
	confFilePath = f"{gladir}/gladitek.json"
	confFileContent = open(confFilePath)
	content = json.load(confFileContent)
	return content['calendars'], content['credentials_path']

# Fetch one Google Calendar
def getCalendarAPI(gladir: str, credentialPath: str, calendarConf):
	return GoogleCalendar(credentials_path=f"{gladir}/{credentialPath}", token_path=f"{gladir}/{calendarConf['token_path']}", calendar=calendarConf['calendar_id'])

# Clears Google calendars
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
	minDateOnFullDump = (1/Jan/(today.year - 2))[0:00]
	maxDate = (1/Jan/(today.year + 2))[0:00]
	for calendarConf in calendarsConf:
		addedEvents = 0
		pedago = calendarConf['pedago']
		calendarAPI = getCalendarAPI(gladir, credentialPath, calendarConf)
		intra = Intra(calendarConf['autologin'])
		print("Loading Intra's Events...")
		if pedago:
			newEvents = intra.getAllEvents(minDateOnFullDump if fullDump else date.today())
		else:
			newEvents = intra.getRegisteredEvents(minDateOnFullDump if fullDump else date.today())
		print("Fetching Google's Events...")
		oldEvents = [oldEvent for oldEvent in calendarAPI.get_events(time_min=minDateOnFullDump if fullDump else date.today(), time_max=maxDate)]
		print("Looking for events to add")
		for event in newEvents:
			if event.title == None:
				continue
			if eventIsKnown(oldEvents, event):
				continue
			registered = not pedago and event.isRegisteredTo()
			assigned = pedago and event.isAssignedTo(intra)
			if not assigned and not registered:
				continue
			print(f"Adding {event.title} to calendar")
			addedEvents += 1
			calendarAPI.add_event(GoogleEvent(event.title, start=event.start, end=event.end, description=event.formatDescription(), location=event.room))
		if addedEvents > 0:
			print(f"Added {addedEvents} events to calendar")
		else:
			print("No event added, up to date!")
