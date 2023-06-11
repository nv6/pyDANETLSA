#!/usr/bin/env python3

import os
import argparse

from pyDANETLSA import DANETLSA_get_supported_protocols


def arguments():
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument("-v", "--verbose",
                        dest='verbose',
                        help="Verbose mode. Default is off",
                        action="store_true",
                        default=False)
    parser.add_argument("-f", "--fqdn",
                        dest='fqdn',
                        help="FQDN",
                        default=None,
                        type=str)
    parser.add_argument("-t", "--transport",
                        dest='transport',
                        help="TCP, UDP or SCTP",
                        choices=['TCP', 'UDP', 'SCTP'],
                        default="TCP",
                        type=str)
    parser.add_argument("-p", "--port",
                        dest='port',
                        help="Port number",
                        default=None,
                        type=int)
    parser.add_argument("-l", "--protocol",
                        dest='protocol',
                        help="Protocol",
                        choices=DANETLSA_get_supported_protocols(),
                        default=None,
                        type=str)

    return parser.parse_args()


def is_startup_clean(args):
    if args.fqdn is None:
        print("Error: no FQDN provided.")
        return False
    
    return True