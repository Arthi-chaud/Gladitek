from gcsa.google_calendar import GoogleCalendar
import json
from datetime import date, datetime, timedelta
from Intra import Intra, Event
from gcsa.event import Event as GoogleEvent

confFilePath = "./gladitek.json"

confFileContent = open(confFilePath)

configuration = json.load(confFileContent)

todayFormat = datetime.now().strftime("%Y-%m-%d")

def eventIsKnown(calendar: GoogleCalendar, newEvent: Event) -> bool:
	for event in calendar:
		if (event.summary == newEvent.title):
			return True
	return False

for calendar in configuration['calendars']:
	intra = Intra(calendar['autologin'])
	newEvents = intra.getAllEvents()
	addedEvents = 0
	calendarAPI = GoogleCalendar(credentials_path=configuration['credentials_path'], token_path=calendar['token_path'], calendar=calendar['calendar_id'])
	calendar = calendarAPI.get_events(time_min=date.today())
	for event in newEvents:
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