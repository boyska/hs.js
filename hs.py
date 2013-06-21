"""
HS utils
"""

import sys
import os
import socket
from contextlib import contextmanager

sys.path.append('libs/torctl/TorCtl')
from stem.control import Controller

class HiddenService(object):
    """Hidden service information are kept here. Not much more"""
    def __init__(self, hsdir, onionport, address):
        self.hsdir = hsdir
        self.onionport = int(onionport)
        self.address = address
        self.onion = get_onion_host_by_dir(hsdir)

def get_onion_host_by_dir(hsdir):
    """Given a path to a directory, assumes it is the directory of a hidden
    service, and return sth like abcdefghij123456.onion"""
    return open(os.path.join(hsdir, 'hostname')).read().strip()

@contextmanager
def get_tor_control(host='127.0.0.1', port=9051):
    """Context manager: yields a connection to the tor control port"""
    with Controller.from_port(port = port) as controller:
        controller.authenticate()
        yield controller


def get_hidden_services():
    """A generator of HiddenService instances"""
    with get_tor_control() as control:
        dirs, ports = sorted(control.get_conf_map('HiddenServiceOptions').items())
        for hsdir, hsport in zip(dirs[1], ports[1]):
            yield HiddenService(hsdir,
                    *hsport.split())

def add_hidden_service(hsdir, onionport, port, host='127.0.0.1'):
    """Add a new hidden service. Does not check if there are conflicts"""
    with get_tor_control() as control:
        curhs_dir, curhs_port = sorted(control.get_conf_map('HiddenServiceOptions').items())
        curhs_dir += (hsdir,)
        curhs_port += ("%d %s:%d" % (onionport,host,port),)
        new = {"HiddenServiceDir": curhs_dir,
              "HiddenServicePort": curhs_port}
        print new
        control.set_options(new)

# vim: set sw=4 sw=4 expandtab:
