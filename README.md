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
$ python3 script.py -t <IP> -p <port> (--ssl if necessary)
```
