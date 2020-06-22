from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def addevent(input):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # GMT_OFF = '-05:00'  # PDT/MST/GMT-7
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for info in input:
        same = False
        date = (info[0]).split('/')
        y, m, d = date[2], date[0], date[1]
        if len(m) == 1:
            m = "0" + m
        if len(d) == 1:
            d = "0" + d

        # This is the information of the Event
        EVENT = {
            'summary': 'Take the book back',
            'start': {'dateTime': '{}-{}-{}T12:00:00-05:00'.format(y, m, d)},
            'end': {'dateTime': '{}-{}-{}T23:59:59-05:00'.format(y, m, d)},
        }

        # Check for events that already in the calendar
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            time = (start.split('T')[0]).split('-')
            cy, cm, cd = time[0], time[1], time[2]
            if (cy == y) and (cm == m) and (cd == d):
                # add into calender if there is no such event
                same = True
                break

        if not same:
            e = service.events().insert(calendarId='primary',
                                        sendNotifications=True, body=EVENT).execute()
