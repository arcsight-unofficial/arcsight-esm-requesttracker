#!/usr/bin/python3
"""Request Tracker Integration.

Making it possible to create tickets in Request Tracker from ArcSight ESM
"""
import os
import argparse
import ConfigParser
import requesttracker as rt
import arcsightesm as esm

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def arguments():
    """Find all arguments.

    Defines all arguments, and performs the action defined in --action

    """
    config_file = ConfigParser.ConfigParser()
    config_file.optionxform = str

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='What action you want, can either be \"new\" or \"test\", other actions added later')
    parser.add_argument('--eventid', help='EventID in ArcSight')
    parser.add_argument('--ticketid', help='ID of the RT Ticket')
    parser.add_argument('--template', help='Which template to use to map ArcSight data to ticket')
    parser.add_argument('--test', help='Test against an specific EventID to see what data it returns')
    args = parser.parse_args()

    if args.template and args.eventid and args.action:
        content = ""
        authtoken = esm.login()
        event = esm.get_event(authtoken, args.eventid)
        config_file.read(os.path.join(ROOT_DIR, 'templates', 'template.conf'))
        payload = {}
        if args.action == 'new':
            for key, values in config_file.items(args.template):
                if values.startswith('arcsight/'):
                    splitvalues = values.replace('arcsight/', '')
                    splitvalues = splitvalues.split('/')
                    details = recursive_search(event, splitvalues, 0, len(splitvalues))
                    if details:
                        payload[key] = details
                    else:
                        payload[key] = "Value not Found"
                else:
                    payload[key] = values
            content += "id: ticket/new\n"
            for k, v in payload.items():
                content += "{}: {}\n".format(k, v)
            rt.new_ticket(content)

        if args.action == 'test':
            for key, values in config_file.items(args.template):
                if values.startswith('arcsight/'):
                    splitvalues = values.replace('arcsight/', '')
                    splitvalues = splitvalues.split('/')
                    details = recursive_search(event, splitvalues, 0, len(splitvalues))
                    if details:
                        payload[key] = details
                    else:
                        payload[key] = "notfound"
                else:
                    payload[key] = values
            for k, v in payload.items():
                content += "{}: {}\n".format(k, v)
            print("This is the event")
            print(event)
    else:
        print("You have not included all mandatory parameters, remember to include action, template and eventid")


def recursive_search(event, lst, list_pointer, list_len):
    """Retrieve events from nested dict.

    Used to check if values in the template exists inside the event dictionary

    Parameters
    ----------
    event : {dict}
        Dictionary of the JSON response from ESM
    lst : {string}
        Configuration value in template.conf
    list_pointer : {int}
        Keeping track of where we are in the iteration
    list_len : {int}
        Total length of nesting inside the dict

    Returns
    -------
    [string]
        Returns the value stored in dict, or False if failing

    """
    if list_pointer == list_len:
        return event
    for k, v in event.items():
        if k == lst[list_pointer]:
            return recursive_search(v, lst, list_pointer + 1, list_len)
    return False


if __name__ == "__main__":
    arguments()
