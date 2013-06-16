from hs import get_hidden_services, add_hidden_service

def hs_list(args):
    print 'List of HS:'
    print '\n'.join((hs.onion for hs in get_hidden_services()))

def hs_add(args):
    import random
    #onionport = random.randint(10000,20000)
    onionport = 12345
    port = 23456
    #port = random.randint(20000,30000)
    add_hidden_service(hsdir='/var/lib/tor/testhey_hs',
            onionport=onionport, port=port)
def hs_rm(args):
    raise NotImplementedError()

import sys
import argparse

parser = argparse.ArgumentParser(prog='hs')
subparsers = parser.add_subparsers(title='subcommands',
        description='valid subcommands', help='additional help')

parser_ls = subparsers.add_parser('list', help='list active hidden services')
parser_ls.set_defaults(func=hs_list)
parser_add = subparsers.add_parser('add', help='add a hidden service')
parser_add.set_defaults(func=hs_add)
parser_rm = subparsers.add_parser('rm', help='remove a hidden service')
parser_rm.set_defaults(func=hs_rm)

args = parser.parse_args(sys.argv[1:])
args.func(args)

