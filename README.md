# SAP Start Service SOAP enumeration

This tool leverage the SAP Start Service SOAP API to exfiltrate information using Python 3.

## What is the SAP Start Service
State by a quote of SAP about the [SAP Start Service](https://help.sap.com/docs/ABAP_PLATFORM/7bbf03267f654b5cb06a8bf78f61fca1/b3903925c34a45e28a2861b59c3c5623.html):

> The SAP start service runs on every computer where an instance of the Application Server ABAP (AS ABAP) is started. It is implemented as a service on Windows, and as a daemon on UNIX. The process is called sapstartsrv.exe on Windows, and sapstartsrv on UNIX platforms.
> The SAP start service provides the following functions for monitoring ABAP systems, application server instances (AS instance), and processes.
> - Starting and stopping
> - Monitoring the runtime state
> - Reading logs, traces, and configuration files
> - Technical information, such as network ports, active sessions, thread lists, etc.
> 
> These functions are provided by the SOAP Web Service interface "SAPControl” and can be executed in SAP monitoring tools, such as SAP Management Console.


## Prerequisits
Install the following requirements:
- suds-community
- argparse
- prettytable

## Setup and run
```bash
$ pip install -r requirements.txt
```
## Usage
```bash
$ python3 sapstartsrv-enum.py -h 
usage: sapstartsrv-enum.py [options]

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
## Example:
- Enumerate unprotected webservices
```bash
python3 sapstartsrv-enum.py -t 127.0.0.1 -p 50013 --methods
```
