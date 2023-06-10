#!/usr/bin/env python3

from libs import constants


def DANETLS_protocol_to_str(protocol):
    if protocol not in constants.DANETLS_protocols:
        raise ValueError("Unknown protocol/method set")

    if   protocol == constants.DANETLSA_IMAP: return "IMAP"
    elif protocol == constants.DANETLSA_POP3: return "POP3"
    elif protocol == constants.DANETLSA_SMTP: return "SMTP"
    elif protocol == constants.DANETLSA_TLS : return "TLS"
    elif protocol == constants.DANETLSA_PEM : return "PEM"
    elif protocol == constants.DANETLSA_DER : return "DER"
    elif protocol == constants.DANETLSA_FTP : return "FTP"

