"""
HS utils
"""

import sys
import os
import socket
from contextlib import contextmanager

sys.path.append('libs/torctl/TorCtl')
from TorCtl import Connection, EventHandler

class HiddenService(object):
    """Hidden service information are kept here. Not much more"""
    def __init__(self, hsdir, onionport, address):
        self.hsdir = hsdir
        self.onionport = onionport
        self.address = address
        self.onion = get_onion_host_by_dir(hsdir)

def get_onion_host_by_dir(hsdir):
    """Given a path to a directory, assumes it is the directory of a hidden
    service, and return sth like abcdefghij123456.onion"""
    return open(os.path.join(hsdir, 'hostname')).read().strip()

@contextmanager
def get_tor_control(host='127.0.0.1', port=9051):
    """Context manager: yields a connection to the tor control port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    conn = Connection(sock)
    conn.set_event_handler(EventHandler())
    conn.launch_thread()
    conn.authenticate()
    yield conn
    conn.close()
    sock.close()

def get_hidden_services():
    """A generator of HiddenService instances"""
    with get_tor_control() as control:
        opt = control.get_option('HiddenServiceOptions')
        if len(opt) == 1:
            return
        for i in xrange(0, len(opt)-1, 2):
            opt_dict = dict((k, v) for (k, v) in opt[i:i+2])
            print 'opt group', opt_dict
            yield HiddenService(opt_dict['HiddenServiceDir'],
                    *opt_dict['HiddenServicePort'].split())

def add_hidden_service(hsdir, onionport, port, host='127.0.0.1'):
    """Add a new hidden service. Does not check if there are conflicts"""
    with get_tor_control() as control:
        curhs = control.get_option('HiddenServiceOptions')
        if len(curhs) == 1:
            curhs = []
        new = curhs + [("HiddenServiceDir", hsdir),
              ("HiddenServicePort", "%d %s:%d" % (onionport,host,port))]
        control.set_options(new)
