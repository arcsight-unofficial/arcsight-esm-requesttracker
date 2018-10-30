#!/usr/bin/python3
"""ArcSight ESM API Endpoints.

All API calls made to ArcSight ESM
"""

import ConfigParser
import json
import requests

CONFIG_FILE = ConfigParser.ConfigParser()
CONFIG_FILE.read('./script.conf')

# RT Configuration
ARCSIGHT_USERNAME = CONFIG_FILE.get('arcsightesm', 'username')
ARCSIGHT_PASSWORD = CONFIG_FILE.get('arcsightesm', 'password')
ARCSIGHT_HOST = CONFIG_FILE.get('arcsightesm', 'hostname')
ARCSIGHT_PORT = CONFIG_FILE.get('arcsightesm', 'port')


def login():
    """Login to ArcSight ESM.

    Retrieves information from script.conf and logs in to ArcSight ESM.

    Returns
    -------
    [string]
        Authentication token

    """
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    payload = {
        "log.login": {
            "log.login": ARCSIGHT_USERNAME,
            "log.password": ARCSIGHT_PASSWORD
        }
    }

    response = requests.post('https://' + ARCSIGHT_HOST + ':' + ARCSIGHT_PORT + '/www/core-service/rest/LoginService/login', json=payload, headers=headers, verify=False)
    response = json.loads(response.text)
    return response['log.loginResponse']['log.return']


def get_event(authtoken, event_id):
    """Retrieve event details.

    Utilizes the authentication token and event id to return all details related to a specific event.

    Parameters
    ----------
    authtoken : {string}
        Authentication token used for API calls.
    event_id : {int}
        Event ID of the event to be returned

    Returns
    -------
    [dict]
        Returns a JSON response, which is turned into a dict before returning it to the main script

    """
    headers = {'accept': 'application/json'}
    payload = {
        'sev.getSecurityEvents': {
            'sev.authToken': authtoken,
            'sev.ids': event_id
        }
    }

    response = requests.post('https://' + ARCSIGHT_HOST + ':' + ARCSIGHT_PORT + '/www/manager-service/rest/SecurityEventService/getSecurityEvents', json=payload, headers=headers, verify=False)
    response = json.loads(response.text)
    if response['sev.getSecurityEventsResponse']['sev.return']:
        return response['sev.getSecurityEventsResponse']['sev.return']
    print('Security Event Not Found')
