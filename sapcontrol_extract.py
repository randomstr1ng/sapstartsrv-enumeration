#!/usr/bin/env python3

from suds.client import Client
from argparse import ArgumentParser
import ssl

def arguments():
        description = "Script to enumerate capabilities of the SAPControl Service"
        usage = "%(prog)s [options]"
        parser = ArgumentParser(usage=usage, description=description)
        target = parser.add_argument_group("Target")
        target.add_argument("-t", "--target", dest="HOST", help="Server Hostname/IP", required=True)
        target.add_argument("-p", "--port", dest="PORT", help="Server Port (Defaut 50013)", default="50013")
        target.add_argument("-s", "--ssl", dest="SSL", action="store_true")
        options = parser.parse_args()
        return options

def build_url(HOST, PORT, SSL):
    if SSL:
        URL = "https://" + str(HOST) + ":" + str(PORT) + "/?wsdl"
    else:
        URL = "http://" + str(HOST) + ":" + str(PORT) + "/?wsdl"
    return URL

def get_instances(URL):
    client = Client(URL)
    instances = client.service.GetSystemInstanceList()
    return instances.item

def get_instance_unportected_methods(URL):
    client = Client(URL)
    properties = client.service.GetInstanceProperties().item
    for property in properties:
        if property.property == "Protected Webmethods":
            p_methods = property.value.split(",")
        elif property.property == "Webmethods":
            methods = property.value.split(",")
        else:
            pass
    u_methods = set(methods) - set(p_methods)
    return u_methods

# main
## ignore invalid SSL certificates
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

## main
options = arguments()
URL = build_url(HOST=options.HOST,PORT=options.PORT,SSL=options.SSL)
print(f"[*] Target URL: {URL}")

instances_list = get_instances(URL=URL)
for instance in instances_list:
    tmp_url = build_url(HOST=options.HOST,PORT=instance.httpPort,SSL=options.SSL)
    unprotected_methods = get_instance_unportected_methods(URL=tmp_url)
    print(f"[+] Unprotected Webmethods: {unprotected_methods}")