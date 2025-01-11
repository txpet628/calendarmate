from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import os
import pickle

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events_past_week():
    creds = None
    # Path to your credentials file
    client_secret_file = '/Users/diana/my_api_secrets/google_calendar_api_secrets.json'
    
    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no credentials are available or invalid, authenticate the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build the service
    service = build('calendar', 'v3', credentials=creds)
    
    # Get the current time and calculate the time one week ago
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    one_week_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat() + 'Z'
    
    # Fetch events from the past week
    events_result = service.events().list(
        calendarId='primary', timeMin=one_week_ago, timeMax=now,
        singleEvents=True, orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    
    # Print the events
    if not events:
        print('No events found in the past week.')
    else:
        print('Events in the past week:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event['summary']}")
    
if __name__ == '__main__':
    get_events_past_week()
