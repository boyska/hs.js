'''
HS utils
'''

import sys
import os
sys.path.append('libs/torctl/TorCtl')
from TorCtl import Connection, DebugEventHandler
import socket

class HiddenService(object):
    '''Hidden service information are kept here. Not much more'''
    def __init__(self, hsdir, onionport, address):
        self.hsdir = hsdir
        self.onionport = onionport
        self.address = address
        self.onion = get_onion_host_by_dir(hsdir)

    @classmethod
    def get_by_onion_port(self, onion, port):
        raise NotImplementedError()

    @classmethod
    def get_by_address(self, host, port):
        raise NotImplementedError()

    @classmethod
    def get_by_dir(self, hsdir):
        raise NotImplementedError()

def get_onion_host_by_dir(hsdir):
    return open(os.path.join(hsdir, 'hostname')).read().strip()

def get_tor_control(host='127.0.0.1', port=9051):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    c = Connection(s)
    c.set_event_handler(DebugEventHandler())
    th = c.launch_thread()
    c.authenticate()
    return c

def get_hidden_services():
    c = get_tor_control()
    opt = c.get_option('HiddenServiceOptions')
    if len(opt) == 1:
        return
    for i in xrange(0, len(opt)-1, 2):
        opt_dict = dict((k,v) for (k,v) in opt[i:i+2])
        print 'opt group', opt_dict
        yield HiddenService(opt_dict['HiddenServiceDir'],
                *opt_dict['HiddenServicePort'].split())

def add_hidden_service(hsdir, onionport, port, host='127.0.0.1'):
    c = get_tor_control()
    curhs = c.get_option('HiddenServiceOptions')
    if len(curhs) == 1:
        curhs = []
    new = curhs + [("HiddenServiceDir", hsdir),
          ("HiddenServicePort", "%d %s:%d" % (onionport,host,port))]
    c.set_options(new)

