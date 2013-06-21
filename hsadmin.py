"""
Simple tool to manage Tor Hidden Services

If you want to create/remove/list hidden services on your tor instance without
messing with your torrc, this is for you.
"""
import argparse
import sys

from hs import get_hidden_services, add_hidden_service
out_buffer = sys.stdout

def hs_list(args):
    """List active hidden services as
    $url.onion:78\t$host:port\t/da/ta/dir
    """
    for hs in get_hidden_services():
	print '%s:%d\t%s\t%s' % \
            (hs.onion, hs.onionport, hs.address, hs.hsdir)

def hs_add(args):
    """Add a hidden service"""
    onionport = int(args.onionport)
    port = int(args.localport)
    add_hidden_service(hsdir='/var/lib/tor/testhey%d_hs' % port,
            onionport=onionport, port=port)
def hs_rm(args):
    """Remove a hidden service"""
    raise NotImplementedError()

def parse_and_run(system_arguments):
    '''Main function'''
    parser = argparse.ArgumentParser(prog='hs')
    subparsers = parser.add_subparsers(title='subcommands',
            description='valid subcommands', help='additional help')

    parser_ls = subparsers.add_parser('list',
            help='list active hidden services')
    parser_ls.set_defaults(func=hs_list)
    parser_add = subparsers.add_parser('add', help='add a hidden service')
    parser_add.add_argument("onionport", help='the port that will be exposed publicly')
    parser_add.add_argument("localport", help='the port the hiddenservice will connect to')
    parser_add.set_defaults(func=hs_add)
    parser_rm = subparsers.add_parser('rm', help='remove a hidden service')
    parser_rm.set_defaults(func=hs_rm)

    args = parser.parse_args(system_arguments)
    args.func(args)

if __name__ == '__main__':
    parse_and_run(sys.argv[1:])
