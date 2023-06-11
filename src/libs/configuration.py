#!/usr/bin/env python3

import os
import argparse
import configparser
import errno


def parse_config_section(ctx, config, section):
    if section not in config.sections():
        print(f"Warning: Configuration file does not have a \"{section}\" section")
        return ctx

    for key in config[section]:
        if 'args_' + key in ctx and ctx['args_' + key] is not None:
            ctx[section + "_" + key] = ctx['args_' + key]
            continue
        else:
            ctx[section + "_" + key] = config[section][key]

    return ctx


def parse_config(ctx):
    config = configparser.ConfigParser()

    

    if not os.path.isfile(ctx['args_configfile']):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), ctx['args_configfile'])

    config.read(ctx['args_configfile'])

    ctx = parse_config_section(ctx, config, 'generic')
    ctx = parse_config_section(ctx, config, 'dnsmasq_dhcp')

    return ctx