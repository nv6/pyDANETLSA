#!/usr/bin/env python3

import OpenSSL.crypto as crypto
import hashlib

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


def x509_to_subject_dn(x509):
    """
    Output in OpenSSL format
    """
    s = ""
    for name, value in x509.get_subject().get_components():
        s = s + '/' + name.decode("utf-8") + '=' + value.decode("utf-8")

    return s


def x509_to_pubkey_key(x509):
    pubkey = crypto.dump_publickey(crypto.FILETYPE_ASN1, x509.get_pubkey())
    m = hashlib.sha256()
    m.update(pubkey)
    m.digest()
    return m.hexdigest()
