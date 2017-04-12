#!/usr/bin/python

import getpass
import os.path
from optparse import OptionParser
import sys
from napalm_cli import Napalm

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="load or write config to file")
parser.add_option("-H", "--host", dest="hostname", help="the host to connecto to")
parser.add_option("-u", "--username", dest="username", default="root", help="the username to use")
parser.add_option("-p", "--port", dest="port", default=22, help="the port to use")
parser.add_option("-t", "--type", dest="devtype", help="which type [ios,iosxr,....]")
parser.add_option("-o", "--operation", dest="operation", help="operation: push (full config), merge (partial config), get, route, cmd")
parser.add_option("-l", "--location", dest="location", help="location: de2, tt4....")
parser.add_option("-r", "--route", dest="route", help="location: de2, tt4....")
parser.add_option("-c", "--command", dest="command", help="any command which will be run at the device")

(options, args) = parser.parse_args()

hostname = options.hostname
username = options.username
password = None
port = options.port
devtype = options.devtype
filename = options.filename
operation = options.operation
location = options.location
route = options.route
command = options.command


if not hostname or not username or not port or not devtype:
    print "Usage: ", sys.argv[0], " -H <host> -u <username> -p <port> -t <type> -o <operation> [-f <filename>] [-l <location>]"
    sys.exit(1)

if not operation:
    print "No operation given."
    sys.exit(1)

if operation == "push" or operation == "merge":
    if options.filename:
        if not os.path.isfile(filename):
            print "File ", filename, " does not exist."
            sys.exit(1)
    if not options.filename:
        print "No filename given."
        sys.exit(1)

if operation == "route":
    if not options.route:
        print "-r option missing"
        sys.exit(1)

if operation == "cmd":
    if not options.command:
        print "-c option missing"
        sys.exit(1)

if not password:
    p = getpass.getpass(prompt="Your Password: ")
else:
    p = password

# connect to device
device = Napalm(hostname, devtype, username, p, port)
device.connect()

if operation == "get":
    if not filename:
	device.show_config(None)
    else:
        device.show_config(filename)

if operation == "push":
    device.push_config(filename)

if operation == "merge":
    device.merge_config(filename)

if operation == "route":
    device.show_route_to(route)

if operation == "cmd":
    commands = command.split(';')
    for cc in commands:
        device.run_cmd(cc)

device.close()

