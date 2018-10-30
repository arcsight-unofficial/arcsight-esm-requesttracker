#!/usr/bin/python3
"""Request Tracker API Endpoints.

All API calls made to Request Tracker
"""

import ConfigParser
import requests

CONFIG_FILE = ConfigParser.ConfigParser()
CONFIG_FILE.read('./script.conf')

RT_USERNAME = CONFIG_FILE.get('requesttracker', 'username')
RT_PASSWORD = CONFIG_FILE.get('requesttracker', 'password')
RT_URL = CONFIG_FILE.get('requesttracker', 'url')


def login():
    """Login to Request Tracker.

    Utilizes the credentials in script.conf to login to RT and return a cookie

    Returns
    -------
    [string]
        returns the cookie to be used in other requests to authenticate

    """
    payload = {'user': RT_USERNAME, 'pass': RT_PASSWORD}
    response = requests.post(RT_URL, data=payload)

    return response.cookies


def new_ticket(fields):
    """Create ticket in Request Tracker.

    Utilizes the cookie from the Login Endpoint, and the content from template.conf to create
    a new ticket.

    Parameters
    ----------
    fields : {string}
        String of content to be added to the ticket.
        Content is added into one form field, separated by newline character for some reason.

    Returns
    -------
    array
        Returns the new ticket ID from RT

    """
    cookie = login()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'content': {fields}
    }

    response = requests.post(RT_URL + 'ticket/new',
                             data=payload, cookies=cookie, headers=headers)
    return response.text


def update_ticket(ticket_id, fields):
    """Still to be implemented.

    Not finished

    Parameters
    ----------
    cookie : {string}
        Cookie

    Returns
    -------
    array
        Returns the new ticket ID from RT

    """
    cookie = login()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'content': {fields}
    }

    response = requests.post(RT_URL + 'ticket/' + ticket_id + '/edit',
                             data=payload, cookies=cookie, headers=headers)
    return response.text
