# SAPControl SOAP utility

This tool leverage the SAPControl SOAP API to exfiltrate information using Python 3.


## Prerequisits
Install the following requirements:
- suds-community
- argparse
- ssl
- prettytable

Example:
```bash
$ pip install -r requirements.txt
```
## Usage
```bash
$ python3 sapcontrol_extract.py -h 
usage: sapcontrol_extract.py [options]

Script to enumerate capabilities of the SAPControl Service

optional arguments:
  -h, --help            show this help message and exit

Target:
  -t HOST, --target HOST
                        Server Hostname/IP
  -p PORT, --port PORT  Server Port (Defaut 50013)
  --ssl
  --user USER           Username for authentication
  --password PASSWORD   Password for authentication
  --instances           Print table of all detected SAP Instances of System
  --methods             Output table of all unprotected SAPControl Methods per Instance
  --services            Output table of running services and ports per Instance (Authenticated)
```
