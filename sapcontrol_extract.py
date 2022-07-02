#!/usr/bin/env python3

from suds.client import Client
from argparse import ArgumentParser
from prettytable import PrettyTable
import ssl

def arguments():
        description = "Script to enumerate capabilities of the SAPControl Service"
        usage = "%(prog)s [options]"
        parser = ArgumentParser(usage=usage, description=description)
        target = parser.add_argument_group("Target")
        target.add_argument("-t", "--target", dest="HOST", help="Server Hostname/IP", required=True)
        target.add_argument("-p", "--port", dest="PORT", help="Server Port (Defaut 50013)", default="50013")
        target.add_argument("--ssl", dest="SSL", action="store_true")
        target.add_argument("--user", dest="USER", help="Username for authentication")
        target.add_argument("--password", dest="PASSWORD", help="Password for authentication")
        target.add_argument("--instances", dest="INSTANCES",help="Print table of all detected SAP Instances of System", action="store_true")
        target.add_argument("--methods", dest="METHODS",help="Output table of all unprotected SAPControl Methods per Instance", action="store_true")
        target.add_argument("--services", dest="SERVICES",help="Output table of running services and ports per Instance (Authenticated)", action="store_true")
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

def get_instance_services(URL, options):
    client = Client(URL, username=options.USER, password=options.PASSWORD)
    services = client.service.GetAccessPointList()
    return services.item

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
if options.INSTANCES:
    print("[+] Instance list:")
    table = PrettyTable(["Hostname", "Instance Nr. ", "Features", "Status"])
    for instance in instances_list:
        table.add_row([instance.hostname, str(instance.instanceNr).zfill(2), instance.features, instance.dispstatus])
    print(table)
if options.SERVICES:
    print("[+] Services per Instance:")
    table = PrettyTable(["Service", "Port", "Protocol"])
    for instance in instances_list:
        if options.SSL:
            tmp_url = build_url(HOST=options.HOST,PORT=instance.httpsPort,SSL=options.SSL)
        else:
            tmp_url = build_url(HOST=options.HOST,PORT=instance.httpPort,SSL=options.SSL)
        services = get_instance_services(URL=tmp_url, options=options)
        print(f"Instance: {instance.hostname}:")
        for service in services:
            table.add_row([service.processname, service.port, service.protocol])
        print(table)
if options.METHODS:
    print("[+] Unprotected WebMethods:")
    table = PrettyTable(["Instance", "Methods"])
    for instance in instances_list:
        if options.SSL:
            tmp_url = build_url(HOST=options.HOST,PORT=instance.httpsPort,SSL=options.SSL)
        else:
            tmp_url = build_url(HOST=options.HOST,PORT=instance.httpPort,SSL=options.SSL)
        unprotected_methods = get_instance_unportected_methods(URL=tmp_url)
        table.add_row([instance.hostname, ",".join(list(unprotected_methods))])
    print(table)
if options.INSTANCES == False and options.METHODS == False:
    print("[-] No Option selected!")