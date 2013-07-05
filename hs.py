"""
HS utils
"""

import os
from contextlib import contextmanager
import logging

from pprint import pformat

from stem.control import Controller

logger = logging.getLogger('hs')

class HiddenService(object):
    """Hidden service information are kept here. Not much more"""
    def __init__(self, hsdir, onionport, address):
        self.hsdir = hsdir
        self.onionport = int(onionport)
        self.address = address
        self.onion = get_onion_host_by_dir(hsdir)
    def __getitem__(self, key):
        return getattr(self, key)

def get_onion_host_by_dir(hsdir):
    """Given a path to a directory, assumes it is the directory of a hidden
    service, and return sth like abcdefghij123456.onion"""
    return open(os.path.join(hsdir, 'hostname')).read().strip()

@contextmanager
def get_tor_control(host='127.0.0.1', port=9051):
    """Context manager: yields a connection to the tor control port"""
    with Controller.from_port(port = port) as controller:
        controller.authenticate()
        logger.debug("got tor controller")
        yield controller


def get_hidden_services():
    """A generator of HiddenService instances"""
    with get_tor_control() as control:
        options = control.get_conf_map('HiddenServiceOptions').items()
        if len(options) == 2:
            dirs, ports = sorted(options)
        elif len(options) < 2:
            return
        else:
            raise Exception("Problems parsing options")
        for hsdir, hsport in zip(dirs[1], ports[1]):
            yield HiddenService(hsdir,
                    *hsport.split())

def add_hidden_service(hsdir, onionport, port, host='127.0.0.1'):
    """Add a new hidden service. Does not check if there are conflicts"""
    with get_tor_control() as control:
        options = control.get_conf_map('HiddenServiceOptions').items()
        logger.debug("current options:\n%s" % pformat(options))
        if len(options) == 2:
            curhs_dir, curhs_port = (o[1] for o in sorted(options))
        elif len(options) < 2:
            curhs_dir = []
            curhs_port = []
        else:
            raise Exception("Problems parsing options")

        curhs_dir += (hsdir,)
        curhs_port += ("%d %s:%d" % (onionport,host,port),)
        new = [("HiddenServiceDir", curhs_dir),
              ("HiddenServicePort", curhs_port)]
        logger.debug('setting options %s' % pformat(new))
        control.set_options(new)

# vim: set sw=4 sw=4 expandtab:
