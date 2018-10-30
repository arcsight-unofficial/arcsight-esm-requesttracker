# ArcSight ESM Request Tracker integration

This application is used to automatically create and update tickets in ([Request Tracker](https://bestpractical.com/request-tracker/)) from ArcSight ESM.

Current status: Working as intended but being improved


## TODO LIST
While the application works as intended, there is several parts that could be made better, planned features are:
* Adding new events to existing tickets (Almost done)
* Proper Logging and configurable logging directory
* Better templating, or support for multiple template files
* Better Error checking on API requests
* Debug mode


## Requirements
Outside of python version 2.7 or 3.x this application requires python-requests for it's API requests, for more information or support please look at their guide ([here](http://docs.python-requests.org/en/master/)) for more information.

If you are not experienced with either python or pip/easy_install i would recommend just installing the current available version from your repository (apt/yum) like so:

YUM:
```sh
$ sudo yum install python-requests
```

APT:
```sh
$ sudo apt-get install python-requests
```


## Installation


### Downloading the application
Download the required package directly from github, either from cli using:
```sh
$ git clone https://github.com/P1llus/arcsight-esm-requesttracker
```
Or if you do not have internet access or proxy connection on the ESM server, download the newest release and move it to the ESM through SCP/RDP
([Releases can be found here](https://github.com/P1llus/arcsight-esm-requesttracker/releases))


### Placing the application on your server
The application itself can be placed anywhere on your server, as long as the user "arcsight" has full access and ownership of the files. In this example i have placed it in `/opt/scripts/requesttracker/`

```sh
$ chown arcsight:arcsight /opt/scripts/requesttracker -R
```


### Installing the custom modules
To ensure that all modules are available from everywhere, start by going into the root directory and run setup.py, this will add the custom modules to your python list-packages folder, so that python knows where they are.
ENSURE YOU ARE USING THE ARCSIGHT USER.

```sh
$ cd /opt/scripts/requesttracker
$ python setup.py install --user
```


### Adding credentials
Copy the configuration file and removing the "example" part in the name, continue to fill out all revelant information like username, password and URL/Hostname of ESM and RT.

```sh
$ cp /opt/scripts/requesttracker/arcsightrequesttracker/config/script.example.conf /opt/scripts/requesttracker/config/script.conf
$ vi /opt/scripts/requesttracker/arcsightrequesttracker/config/script.conf
```


### Basic Template
Make a copy of the example template, and remove the "example" part of the filename

```sh
$ cp /opt/scripts/requesttracker/arcsightrequesttracker/templates/template.example.conf /opt/scripts/requesttracker/templates/template.conf
$ vi /opt/scripts/requesttracker/arcsightrequesttracker/templates/template.conf
```

To get started, try to create just a basic template without any custom fields, so remove all content in the template, and create something like this. This is the minimum amount of mandatory fields required to create a ticket, including:
* [Bruteforce] = The name of your template. As the examples show, you can add as many templates as you want.
* Queue = Which queue in Request Tracker you want to create the ticket in
* Requestor = Who created the ticket
* Priority = Ticket priority
* Subject = Title of the ticket
```

[Bruteforce]
Queue=General
Requestor=root@localhost
Priority=4
Subject=Test ticket
```

Some examples have been added to show how it looks like in the end to `/opt/scripts/requesttracker/arcsightrequesttracker/templates/templates.example.conf`
```
[Bruteforce]
Queue=General
Requestor=root@localhost
Priority=arcsight/priority
Subject=arcsight/name
CF-SourceIP=arcsight/source/address
CF-DestinationIP=arcsight/destination/address
CF-Username=arcsight/file/fileName
CF-NetworkZone=arcsight/device/zone/uri

[Antivirus]
Queue=General
Requestor=root@localhost
Priority=4
Subject="Antivirus Agent has been triggered"
CF-SourceIP=arcsight/source/address
CF-DestinationIP=arcsight/destination/address
CF-Virus=arcsight/deviceCustomString1
```


## Running the script


### Testing the ESM and Request Tracker connection
To test that the script can communicate with ArcSight ESM, and to get a full list of all mappings available for the template you can now run this command(Remember to get a currently available eventID from ESM, and the template name is what you configured in your template.conf):

```sh
$ cd /opt/scripts/requesttracker/arcsightrequesttracker/
$ python main.py --action test --eventid 123123 --template Bruteforce
```

The output from this should be printing out all details available about the event, example below:

```json
{u'agent': {u'address': 3232236066,
            u'addressAsBytes': u'wKgCIg==',
            u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
            u'assetLocalId': 17179869185,
            u'assetName': u'arcsight',
            u'hostName': u'arcsight',
            u'id': u'3aNobyWQBABCAYb0cP6Sxtw==',
            u'macAddress': -9223372036854775808,
            u'mutable': True,
            u'name': u'Manager Internal Agent',
            u'translatedAddress': -9223372036854775808,
            u'type': u'arcsight_security_manager',
            u'version': u'6.11.0.2339.0',
            u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                      u'isModifiable': False,
                      u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                      u'referenceID': 1091,
                      u'referenceName': u'Zone',
                      u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                      u'referenceType': 29,
                      u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'agentReceiptTime': -9223372036854775808,
 u'agentSeverity': 1,
 u'aggregatedEventCount': 1,
 u'assetCriticality': 0,
 u'baseEventCount': 0,
 u'bytesIn': -2147483648,
 u'bytesOut': -2147483648,
 u'category': {u'behavior': u'/Execute/Query',
               u'deviceGroup': u'/Application',
               u'mutable': True,
               u'object': u'/Host/Application',
               u'outcome': u'/Success',
               u'significance': u'/Informational'},
 u'concentratorAgents': {u'address': 3232236066,
                         u'addressAsBytes': u'wKgCIg==',
                         u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                         u'assetLocalId': 17179869185,
                         u'assetName': u'arcsight',
                         u'hostName': u'arcsight',
                         u'id': u'3aNobyWQBABCAYb0cP6Sxtw==',
                         u'macAddress': -9223372036854775808,
                         u'mutable': True,
                         u'name': u'Manager Internal Agent',
                         u'translatedAddress': -9223372036854775808,
                         u'type': u'arcsight_security_manager',
                         u'version': u'6.11.0.2339.0',
                         u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                                   u'isModifiable': False,
                                   u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                                   u'referenceID': 1091,
                                   u'referenceName': u'Zone',
                                   u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                                   u'referenceType': 29,
                                   u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'concentratorDevices': {u'address': 3232236066,
                          u'addressAsBytes': u'wKgCIg==',
                          u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                          u'assetLocalId': 17179869185,
                          u'assetName': u'arcsight',
                          u'hostName': u'arcsight',
                          u'macAddress': -9223372036854775808,
                          u'mutable': True,
                          u'product': u'ArcSight',
                          u'translatedAddress': -9223372036854775808,
                          u'vendor': u'ArcSight',
                          u'version': u'6.11.0.2339.0',
                          u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                                    u'isModifiable': False,
                                    u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                                    u'referenceID': 1091,
                                    u'referenceName': u'Zone',
                                    u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                                    u'referenceType': 29,
                                    u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'correlatedEventCount': 0,
 u'destination': {u'address': 3232236066,
                  u'addressAsBytes': u'wKgCIg==',
                  u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                  u'assetLocalId': 17179869185,
                  u'assetName': u'arcsight',
                  u'geo': {u'latitude': 0,
                           u'latitudeLong': 0,
                           u'longitude': 0,
                           u'longitudeLong': 0,
                           u'mutable': True},
                  u'hostName': u'arcsight',
                  u'macAddress': -9223372036854775808,
                  u'mutable': True,
                  u'port': -2147483648,
                  u'processId': -2147483648,
                  u'translatedAddress': -9223372036854775808,
                  u'translatedPort': -2147483648,
                  u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                            u'isModifiable': False,
                            u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                            u'referenceID': 1091,
                            u'referenceName': u'Zone',
                            u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                            u'referenceType': 29,
                            u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'device': {u'address': 3232236066,
             u'addressAsBytes': u'wKgCIg==',
             u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
             u'assetLocalId': 17179869185,
             u'assetName': u'arcsight',
             u'hostName': u'arcsight',
             u'macAddress': -9223372036854775808,
             u'mutable': True,
             u'product': u'ArcSight',
             u'translatedAddress': -9223372036854775808,
             u'vendor': u'ArcSight',
             u'version': u'6.11.0.2339.0',
             u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                       u'isModifiable': False,
                       u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                       u'referenceID': 1091,
                       u'referenceName': u'Zone',
                       u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                       u'referenceType': 29,
                       u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'deviceCustom': {u'date1Label': u'Channel interval start',
                   u'date2Label': u'Channel interval end',
                   u'mutable': True,
                   u'number1Label': u'Number of queries issued',
                   u'number2Label': u'Number of events in channel',
                   u'number3Label': u'Query time in seconds',
                   u'string1Label': u'Channel query',
                   u'string2Label': u'Configuration Resource'},
 u'deviceCustomDate1': 1540717877000,
 u'deviceCustomDate2': 1540721477000,
 u'deviceCustomFloatingPoint1': 5e-324,
 u'deviceCustomFloatingPoint2': 5e-324,
 u'deviceCustomFloatingPoint3': 5e-324,
 u'deviceCustomFloatingPoint4': 5e-324,
 u'deviceCustomNumber1': 6,
 u'deviceCustomNumber2': 1521,
 u'deviceCustomNumber3': 2,
 u'deviceCustomString1': u'select /* Generate Stataticstics Query for Channel name=System Events Last Hour, channelID=QjZvvPPsAABCAEcWZ6-B1EQ==, sessionID=11un8a5l3a85c1ae0-a60e-4718-91da-d8ddeb36ebfb */  DATE_FORMAT(event1.end_time,\'%Y-%m-%d %H:%i\') "Minute(End Time)",event1.priority "Priority",count(event1.event_id) "Count(Event ID)" from  arc_event event1  where 1=1  and (event1.end_time >= \'2018-10-28 09:11:17.000\' and event1.end_time < \'2018-10-28 10:11:17.000\') and ( 1 = 1  and (((event1.event_type IS NULL Or event1.event_type != 2) and event1.dvc_product = BINARY \'ArcSight\' and event1.dvc_vendor = BINARY \'ArcSight\') or (event1.dvc_product = BINARY \'ArcSight\' and event1.dvc_vendor = BINARY \'ArcSight\' and not(event1.locality is null) and (event1.locality IS NULL Or event1.locality != 1) and event1.dvc_event_cat',
 u'deviceCustomString2': u'<Resource URI="/All Active Channels/ArcSight Administration/ESM/System Health/Events/System Events Last Hour" ID="QjZvvPPsAABCAEcWZ6-B1EQ=="/>',
 u'deviceDirection': -2147483648,
 u'deviceEventCategory': u'/Active Channel/QueryCompleted',
 u'deviceEventClassId': u'channel:003',
 u'deviceProcessId': -2147483648,
 u'deviceReceiptTime': 1540721479589,
 u'deviceSeverity': u'Warning',
 u'domainDate1': -9223372036854775808,
 u'domainDate2': -9223372036854775808,
 u'domainDate3': -9223372036854775808,
 u'domainDate4': -9223372036854775808,
 u'domainDate5': -9223372036854775808,
 u'domainDate6': -9223372036854775808,
 u'domainFp1': 5e-324,
 u'domainFp2': 5e-324,
 u'domainFp3': 5e-324,
 u'domainFp4': 5e-324,
 u'domainFp5': 5e-324,
 u'domainFp6': 5e-324,
 u'domainFp7': 5e-324,
 u'domainFp8': 5e-324,
 u'domainIpv4addr1': -9223372036854775808,
 u'domainIpv4addr2': -9223372036854775808,
 u'domainIpv4addr3': -9223372036854775808,
 u'domainIpv4addr4': -9223372036854775808,
 u'domainNumber1': -9223372036854775808,
 u'domainNumber10': -9223372036854775808,
 u'domainNumber11': -9223372036854775808,
 u'domainNumber12': -9223372036854775808,
 u'domainNumber13': -9223372036854775808,
 u'domainNumber2': -9223372036854775808,
 u'domainNumber3': -9223372036854775808,
 u'domainNumber4': -9223372036854775808,
 u'domainNumber5': -9223372036854775808,
 u'domainNumber6': -9223372036854775808,
 u'domainNumber7': -9223372036854775808,
 u'domainNumber8': -9223372036854775808,
 u'domainNumber9': -9223372036854775808,
 u'endTime': 1540721479589,
 u'eventAnnotation': {u'auditTrail': u'1,1539102087491,root,Queued,,,,\n',
                      u'endTime': 1540721479589,
                      u'eventId': 198236,
                      u'flags': 0,
                      u'managerReceiptTime': 1540721479589,
                      u'modificationTime': 1540721479664,
                      u'stage': {u'id': u'R9MHiNfoAABCASsxbPIxG0g==',
                                 u'isModifiable': False,
                                 u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                                 u'referenceID': 2209,
                                 u'referenceName': u'Stage',
                                 u'referenceString': u'<Resource URI="/All Stages/Queued" ID="R9MHiNfoAABCASsxbPIxG0g=="/>',
                                 u'referenceType': 34,
                                 u'uri': u'/All Stages/Queued'},
                      u'stageUpdateTime': 1540721479664,
                      u'version': 1},
 u'eventId': 198236,
 u'file': {u'createTime': -9223372036854775808,
           u'modificationTime': -9223372036854775808,
           u'name': u'System Events Last Hour',
           u'path': u'/All Active Channels/ArcSight Administration/ESM/System Health/Events/System Events Last Hour',
           u'size': -9223372036854775808,
           u'type': u'ActiveChannel'},
 u'finalDevice': {u'address': 3232236066,
                  u'addressAsBytes': u'wKgCIg==',
                  u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                  u'assetLocalId': 17179869185,
                  u'assetName': u'arcsight',
                  u'hostName': u'arcsight',
                  u'macAddress': -9223372036854775808,
                  u'mutable': True,
                  u'product': u'ArcSight',
                  u'translatedAddress': -9223372036854775808,
                  u'vendor': u'ArcSight',
                  u'version': u'6.11.0.2339.0',
                  u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                            u'isModifiable': False,
                            u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                            u'referenceID': 1091,
                            u'referenceName': u'Zone',
                            u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                            u'referenceType': 29,
                            u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'flexDate1': -9223372036854775808,
 u'flexNumber1': -9223372036854775808,
 u'flexNumber2': -9223372036854775808,
 u'locality': 0,
 u'managerId': -128,
 u'managerReceiptTime': 1540721479589,
 u'modelConfidence': 4,
 u'name': u'Channel [System Events Last Hour] query completed',
 u'originalAgent': {u'address': 3232236066,
                    u'addressAsBytes': u'wKgCIg==',
                    u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                    u'assetLocalId': 17179869185,
                    u'assetName': u'arcsight',
                    u'hostName': u'arcsight',
                    u'id': u'3aNobyWQBABCAYb0cP6Sxtw==',
                    u'macAddress': -9223372036854775808,
                    u'mutable': True,
                    u'name': u'Manager Internal Agent',
                    u'translatedAddress': -9223372036854775808,
                    u'type': u'arcsight_security_manager',
                    u'version': u'6.11.0.2339.0',
                    u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                              u'isModifiable': False,
                              u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                              u'referenceID': 1091,
                              u'referenceName': u'Zone',
                              u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                              u'referenceType': 29,
                              u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
 u'originator': u'SOURCE',
 u'persistence': -2147483648,
 u'priority': 3,
 u'relevance': 10,
 u'sessionId': -9223372036854775808,
 u'severity': 0,
 u'startTime': 1540721477546,
 u'ttl': 10,
 u'type': u'BASE'}
```


This means that the ArcSight ESM connection is working, so let's also test the RequestTracker connection by creating a test ticket:


```sh
$ cd /opt/scripts/requesttracker/arcsightrequesttracker/
$ python main.py --action new --eventid 123123 --template Bruteforce
```
This should generate a new ticket in the RequestTracker Queue defined in your template. If any errors occured, please look in the troubleshoot section at the end.


### Advanced Templating
It is possible to map information from the original correlated event triggered by ESM, when running the test above, you are able to see all mappings available as a value in your ticket. If the value is not available, it will display "Value not found" in your ticket upon creation.


As you can see from the event example, certain information are "nested", example the URI of an original agent:
```json
u'originalAgent': {u'address': 3232236066,
                    u'addressAsBytes': u'wKgCIg==',
                    u'assetId': u'47tkbyWQBABCAWGckpuf3CQ==',
                    u'assetLocalId': 17179869185,
                    u'assetName': u'arcsight',
                    u'hostName': u'arcsight',
                    u'id': u'3aNobyWQBABCAYb0cP6Sxtw==',
                    u'macAddress': -9223372036854775808,
                    u'mutable': True,
                    u'name': u'Manager Internal Agent',
                    u'translatedAddress': -9223372036854775808,
                    u'type': u'arcsight_security_manager',
                    u'version': u'6.11.0.2339.0',
                    u'zone': {u'id': u'M-fU32AABABCDVFpYAT3UdQ==',
                              u'isModifiable': False,
                              u'managerID': u'PtobyWQBABCAWwH8uGGm-Q==',
                              u'referenceID': 1091,
                              u'referenceName': u'Zone',
                              u'referenceString': u'<Resource URI="/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255" ID="M-fU32AABABCDVFpYAT3UdQ=="/>',
                              u'referenceType': 29,
                              u'uri': u'/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 192.168.0.0-192.168.255.255'}},
```
For example, if you want to map the agents URI, which is located in OriginalAgent, Zone, URI, this is added to your template using "arcsight/FULLPATH", in this case it would be =arcsight/originalAgent/zone/uri.
For more mapping examples, see the example templates.

So basically all information that are hardcoded text, you fill in normally in the template, and everytime you want to reference the value inside the ArcSight Event, you start it with `arcsight/Something/nestedvalue/anothernestedvalue`.

Recommended to run another ticket creation test, to ensure all new template mappings are working.


### Automatic Ticket from ESM Correlation Rule
This expects that you are now able to run both the test action and new ticket command manually without errors.
Login to your ESM Console, and create a new rule, or edit an existing one.

Under the action tab of your rule, right click, add and choose `Execute Command`.

Fill in the correct information related to your environment:
* Platform - The current OS and distribution you are running.
* Command - The command you want to run when the rule triggers, without parameters.
* Parameters - The actions you want to send to the script when it runs, remember to include $eventId here.
* Action Type - How it should execute

Here is an example of how it would look like:
![executecommand](https://imgur.com/AslpAGR)

Try to trigger the rule to ensure that the ticket is created in the end.


### Manually triggering ticket creation from ESM Console
To be able to right click an event, and create a ticket you would need to create an integration command.
This varies a bit from version to version, so if there is any issues creating integration commands i would recommend looking into the Console User Guide for ArcSight ESM for more information.

This command runs from the your own local machine where the client is installed, which means that the server or client used to access the ESM would need all the requirements specified at the start of the documentation.
If all requirements like python and such is installed, create a new integration command and fill in the same parameters as when creating an automatic rule:

![manualexecute](https://imgur.com/a/667SCdb)


### But what if i don't want to install things on my management server?
Then it's time to be creative, here are some pointers that will push you in the right direction:
Integration commands creates an internal event called "integrationcommand:101", you can create an empty integration command and a rule that triggers on this activity to still run the script from the server itself.

Another option is CounterACT connectors as a destination for your integration command target.


## Troubleshooting
This list will grow bigger once further testing and feedback has been received.

* My ticket is never created:
Try to run the the script from commandline, to see which error it gives you back.

* My ticket has empty values:
Make sure the field type is correct. If the field in Request Tracker i set to IP Address, but you are sending it text, this will show up as empty.
If the value is "No value found" it means that the information is empty in the ArcSight event and you might need to add the field to your aggregation.


## Reporting bugs
If you find any bugs that you want to report, please create a github issue including your python version, ESM version and the returned errors together with a description of how to reproduce it.


## Contributing
If you spot errors or parts that needs improvements, feel free to create a fork and a Pull Request with additional changes.
If you want to contribute but do not know what to work on, feel free to look at the TODO list at the top or currently open issues.
All code should pass PEP-8 and flake linting beforehand, certain exceptions are allowed, but try to keep it consistent