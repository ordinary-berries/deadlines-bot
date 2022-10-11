import datetime
import os.path

import config as cfg
from logger import Log

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CalendarAPI:
    def __init__(self, log):
        """
        :param log: Logger object
        """

        self.logger = log

        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        self.creds = None
        self.service = None
        self.calendar_id = cfg.CALENDAR_ID

        self._build_service()
        
        self.logger.info('CalendarAPI initialized')

    def get_events_data(self, max_days=7) -> list:

        """
        Returns a list of events with the following data:
        - summary (title)
        - start (start date)
        - end (end date)
        sample output:
        [{'summary': '2 лабы по оп', 'start': '2022-10-11T20:30:00+03:00', 'end': '2022-10-11T21:30:00+03:00'},
        {'summary': 'дз на сортми', 'start': '2022-10-11T22:00:00+03:00', 'end': '2022-10-11T23:00:00+03:00'},
        {'summary': 'Дз линал ', 'start': '2022-10-12T21:30:00+03:00', 'end': '2022-10-12T22:30:00+03:00'},
        {'summary': 'Коллоквиум дискретка ', 'start': '2022-10-13T19:00:00+03:00', 'end': '2022-10-13T20:15:00+03:00'},
        {'summary': 'типовик дискретка', 'start': '2022-10-16T21:00:00+03:00', 'end': '2022-10-16T22:00:00+03:00'},
        {'summary': 'Гит лабораторная', 'start': '2022-10-18T22:15:00+03:00', 'end': '2022-10-18T23:15:00+03:00'},
        {'summary': 'Кр матан', 'start': '2022-10-21T10:00:00+03:00', 'end': '2022-10-21T11:00:00+03:00'}]

        First authorization will require you to authenticate in your browser

        """

        events = self._get_upcoming_events(max_days=max_days)
        events_data = []
        for event in events:
            start = event['start'].get('dateTime', event['s=7tart'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            events_data.append({'summary': event['summary'], 'start': start, 'end': end})
        return events_data

    def _get_upcoming_events(self, max_days=7) -> dict:
        """
        Returns a list of upcoming events
        :param max_days: Max days to look ahead for events
        :return: Upcoming events from google calendar
        """
        self.logger.info('Getting upcoming events')
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        max_date = (datetime.datetime.utcnow() + datetime.timedelta(days=max_days)).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now, timeMax=max_date,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        self.logger.info(f'Found {len(events)} events')
        return events

    def _get_creds(self) -> None:
        """
        Gets credentials from token file or creates a new one
        :return:
        """
        self.logger.info('Getting credentials')
        if os.path.exists(cfg.TOKEN_FILE_PATH):
            self.logger.info('Token file found')
            self.creds = Credentials.from_authorized_user_file(cfg.TOKEN_FILE_PATH, self.SCOPES)
        else:
            self.logger.info('Token file not found')
            self._check_creds()

    def _check_creds(self) -> None:
        """
        Checks if credentials are valid, if not, creates a new one
        :return:
        """
        self.logger.info('Checking credentials')
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if os.path.exists(cfg.CREDENTIALS_FILE_PATH):
                    self.logger.info('Credentials file found')
                    flow = InstalledAppFlow.from_client_secrets_file(cfg.CREDENTIALS_FILE_PATH, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    self.logger.error('Credentials file not found')
                    raise FileNotFoundError('Credentials file not found')
                flow = InstalledAppFlow.from_client_secrets_file(cfg.CREDENTIALS_FILE_PATH, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
                self.logger.info('Saved credentials')
            with open(cfg.TOKEN_FILE_PATH, 'w') as token:
                self.logger.info('Saving token')
                token.write(self.creds.to_json())
                self.logger.info('Token saved')

    def _build_service(self) -> None:
        """
        Builds the service
        :return:
        """
        self.logger.info('Building service')
        self._get_creds()
        self.service = build('calendar', 'v3', credentials=self.creds, cache_discovery=False)
        self.logger.info('Service built')


if __name__ == '__main__':
    logger = Log()
    cal = CalendarAPI(logger)
    print(cal.get_events_data(12))

