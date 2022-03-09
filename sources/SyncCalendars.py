from locale import normalize
from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, datetime, timedelta
from sources.Intra import Intra, Event
from gcsa.event import Event as GoogleEvent

todayFormat = datetime.now().strftime("%Y-%m-%d")

def eventIsKnown(calendar: GoogleCalendar, newEvent: Event) -> bool:
	for event in calendar:
		if (event.summary == newEvent.title):
			return True
	return False

def syncCalendars(gladir: str, redump: bool):
	confFilePath = f"{gladir}/gladitek.json"
	confFileContent = open(confFilePath)
	configuration = json.load(confFileContent)
	for calendar in configuration['calendars']:
		addedEvents = 0
		calendarAPI = GoogleCalendar(credentials_path=f"{gladir}/{configuration['credentials_path']}", token_path=f"{gladir}/{calendar['token_path']}", calendar=calendar['calendar_id'])
		if redump:
			print("Clearing calendar...")
			for event in calendarAPI.get_events():
				calendarAPI.delete_event(event.id)
			print("Calendar cleared!")
		intra = Intra(calendar['autologin'])
		newEvents = intra.getAllEvents(date(2015, 1, 1) if redump else date.today())
		calendar = calendarAPI.get_events(time_min=date.today())
		for event in newEvents:
			if event.title == None:
				continue
			if not event.isAssignedTo(intra) and not event.isRegisteredTo():
				continue
			if eventIsKnown(calendar, event):
				continue
			print(f"Adding {event.title} to calendar")
			addedEvents += 1
			calendarAPI.add_event(GoogleEvent(event.title, start=event.start, end=event.end, description=event.getUrl(), location=event.room))
		if addedEvents > 0:
			print(f"Added {addedEvents} events to calendar")
		else:
			print("No event added, up to date!")
