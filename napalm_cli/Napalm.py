import sys
import re
import pprint
from napalm_base import get_network_driver

class Napalm(object):
    def __init__(self, hostname, model, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.model = model
        self.device = None

    def connect(self):
        driver = get_network_driver(self.model)
        self.device = driver(hostname=self.hostname, username=self.username, password=self.password, optional_args={'port': self.port})
        self.device.open()

    def close(self):
        self.device.close()
        return 0

    def push_config(self, filename):
        try:
            self.device.load_replace_candidate(filename=filename)
        except:
            print "Error: Couldn't load configuration. "
            raise
        else:
            self.device.commit_config()

    def merge_config(self, filename):
        try:
            self.device.load_merge_candidate(filename=filename)
        except:
            print "Error Couldn't merge configuration. "
            raise
        else:
            self.device.commit_config()


    def show_config(self, filename):
        config = self.device.get_config(retrieve=u'running')
        if not filename:
            clean = re.sub('.*Building configuration...', '', config['running'].replace('\\n', '\n'))
            print clean
        else:
            try:
                clean = re.sub('.*Building configuration...', '', config['running'].replace('\\n', '\n'))
                ff = open(filename, 'w')
                ff.write(clean)
                ff.close()
            except IOError:
                print "Error: Couldn't open file ", filename
                raise

    def show_route_to(self, destination):
        if self.model == "iosxr":
            routes = self.device.get_route_to(destination=destination, protocol='static')
            for r in routes:
                for dest in routes[r]:
                    if dest['current_active']:
                        print "ACTIVE\t" + r + " to " + dest['next_hop']
                    else:
                        print "DOWN\t" + r + " to " + dest['next_hop']
        else:
            print "Sorry not implemented"

    def run_cmd(self, command):
        result = self.device.cli([command])
        clean = result[command].replace('\\n', '\n')
        print clean
