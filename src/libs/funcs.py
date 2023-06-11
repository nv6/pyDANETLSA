#!/usr/bin/env python3

import OpenSSL.crypto as crypto
import hashlib



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
