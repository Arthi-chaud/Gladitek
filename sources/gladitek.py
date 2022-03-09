from xmlrpc.client import DateTime
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
import json
import requests
from datetime import datetime
from Intra import Intra
from gcsa.event import Event as GoogleEvent

confFilePath = "./setup.json"

confFileContent = open(confFilePath)

configuration = json.load(confFileContent)

todayFormat = datetime.now().strftime("%Y-%m-%d")

for calendar in configuration['calendars']:
	intra = Intra(calendar['autologin'])
	events = intra.getAllEvents()
	addedEvents = 0
	calendarAPI = GoogleCalendar(credentials_path=configuration['credentials_path'], token_path=calendar['token_path'], calendar=calendar['calendar_id'])
	for event in events:
		if not event.isAssignedTo(intra) and not event.isRegisteredTo():
			continue
		if len(list(filter(lambda prevEvent: event.title == prevEvent.summary, calendarAPI))) != 0:
			continue
		print(f"Adding {event.title} to calendar")
		addedEvents += 1
		calendarAPI.add_event(GoogleEvent(event.title, start=event.start, end=event.end, description=event.getUrl(), location=event.room))
	if addedEvents > 0:
		print(f"Added {addedEvents} to calendar")
	else:
		print("No event added, up to date!")