"""
Simple tool to manage Tor Hidden Services

If you want to create/remove/list hidden services on your tor instance without
messing with your torrc, this is for you.
"""
import argparse
import sys
import logging

from hs import get_hidden_services, add_hidden_service
from hs import logger as hs_logger
out_buffer = sys.stdout


def hs_list(args):
    """List active hidden services according to args.fmt"""
    for hs in get_hidden_services():
        print args.fmt.replace(r'\t', '\t') % hs
hs_list.default_format = r'%(onion)s:%(onionport)d\t%(address)s\t%(hsdir)s'

def hs_add(args):
    """Add a hidden service"""
    onionport = int(args.onionport)
    port = int(args.localport)
    hsdir = args.hsdir if args.hsdir is not None else\
        '/var/lib/tor/testhey%d_hs' % port
    add_hidden_service(hsdir=hsdir,
                       onionport=onionport, port=port)


def hs_rm(args):
    """Remove a hidden service"""
    raise NotImplementedError()


def setup_logger(logger):
    #TODO: add option
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def parse_and_run(system_arguments):
    '''Main function'''

    parser = argparse.ArgumentParser(prog='hs')
    parser.add_argument("--debug", action="store_true", default=False)
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')

    parser_ls = subparsers.add_parser('list',
                                      help='list active hidden services')
    parser_ls.set_defaults(func=hs_list)
    parser_ls.add_argument("-f", "--format",
                           help='line format, default is ' +
                           hs_list.default_format.replace('%',
                                                          '%%'),
                           dest="fmt",
                           default=hs_list.default_format
                           )
    parser_add = subparsers.add_parser('add', help='add a hidden service')
    parser_add.add_argument("onionport",
                            help='the port that will be exposed publicly')
    parser_add.add_argument("localport", help='the port the hiddenservice will connect to')
    parser_add.add_argument("-d", "--hsdir", help='the directory of the hidden service')
    parser_add.set_defaults(func=hs_add)
    parser_rm = subparsers.add_parser('rm', help='remove a hidden service')
    parser_rm.set_defaults(func=hs_rm)

    args = parser.parse_args(system_arguments)
    if args.debug:
        setup_logger(hs_logger)
    args.func(args)

if __name__ == '__main__':
    parse_and_run(sys.argv[1:])
