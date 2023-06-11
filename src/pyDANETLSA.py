#!/usr/bin/env python3

import os
import ssl
import ftplib
import imaplib
import poplib
import smtplib
import OpenSSL.crypto as crypto
from enum import Enum

from libs import funcs
from libs import dnstools


class DANETLSAprotocols(Enum):
    DANETLSA_IMAP = 10
    DANETLSA_POP3 = 20
    DANETLSA_SMTP = 30
    DANETLSA_TLS  = 40
    DANETLSA_PEM  = 50
    DANETLSA_DER  = 60
    DANETLSA_FTP  = 70    


def DANETLS_protocol_to_str(protocol):
    if protocol not in DANETLSAprotocols:
        raise ValueError("Unknown protocol/method set")

    if   protocol == DANETLSAprotocols.DANETLSA_IMAP: return "IMAP"
    elif protocol == DANETLSAprotocols.DANETLSA_POP3: return "POP3"
    elif protocol == DANETLSAprotocols.DANETLSA_SMTP: return "SMTP"
    elif protocol == DANETLSAprotocols.DANETLSA_TLS : return "TLS"
    elif protocol == DANETLSAprotocols.DANETLSA_PEM : return "PEM"
    elif protocol == DANETLSAprotocols.DANETLSA_DER : return "DER"
    elif protocol == DANETLSAprotocols.DANETLSA_FTP : return "FTP"


def DANETLSA_get_supported_protocols():
    for i in DANETLSAprotocols:
        print(DANETLS_protocol_to_str(i))

    return [DANETLS_protocol_to_str(i) for i in DANETLSAprotocols]


class DANETLSA(object):

    """
    IMAP: StartTLS for IMAP
    POP3: StartTLS for POP3
    SMTP: StartTLS for SMTP
    TLS : Plain TLS protocol, any application protocol
    PEM : Input is a X.509 certificate in PEM format
    DER : Input is a X.509 certificate in DER format
    FTP : StartTLS for FTP
    """
    def __init__(self, fqdn=None, port=None, domain=None,
                       tlsa_protocol='tcp', probe_protocol=DANETLSAprotocols.DANETLSA_TLS,
                       certfile=None):
        if tlsa_protocol.lower() not in ['tcp', 'udp', 'sctp']:
            raise ValueError("Unknown protocol/method set for TLSA output record.")

        if probe_protocol not in DANETLSAprotocols:
            raise ValueError("Unknown protocol/method set for reading/probing.")

        if fqdn is None:
            raise ValueError("No fqdn provided")

        if port is None:
            raise ValueError("No port provided")

        # Fill class with values
        self.fqdn = fqdn
        self.port = port
        self.tlsa_protocol = tlsa_protocol.lower()
        self.probe_protocol = probe_protocol
        self.domain = domain
        self.certfile = certfile

        # Normalization
        if self.fqdn[-1] == '.':
            self.fqdn = self.fqdn[:-1]

        if self.domain is None:
            # Chop last two domain elements off, zone with TLD
            self.host = ".".join(self.fqdn.split('.')[:-2])

            self.domain = ".".join([self.fqdn.split('.')[-2],
                                    self.fqdn.split('.')[-1]])
        else:
            # Normalize
            if self.domain[-1] == '.':
                self.domain = self.domain[:-1]

            self.host = ".".join(self.fqdn.split('.')[:-len(self.domain.split('.'))])

        # Check if the file exists
        if self.certfile is not None:
            if not os.path.exists(self.certfile):
                raise IOError("file '{}' does not exist.".format(self.certfile))
            if not os.path.isfile(self.certfile):
                raise IOError("file '{}' is not a file.".format(self.certfile))

        print("initialized")

    def dns_tlsa(self):
        # Parse and construct config for dnspython
        dns_config = dnstools.DnsPythonConfig("192.168.1.2")
        status, answers = dnstools.dns_query(self.tlsa_rr_name_fqdn(),
                                    'TLSA', 
                                    dns_config,
                                    False)
        if status != dnstools.DNSERRORS.NOERROR:
            return None

        return sorted([str(rr) for rr in answers])

    def match_cert_with_tlsa_rr(self):
        dns_tlsa_list = self.dns_tlsa()
        x509_tlsa_3_1_1 = self.tlsa_rdata_3_1_1()

        if dns_tlsa_list is None:
            return False

        for rr in dns_tlsa_list:
            if x509_tlsa_3_1_1 == rr:
                return True
        else:
            return False


    def pubkey_hex(self):
        return funcs.x509_to_pubkey_key(self.x509)

    def subject_dn(self):
        return funcs.x509_to_subject_dn(self.x509)

    def tlsa_rdata_3_1_1(self):
        return "3 1 1 " + self.pubkey_hex()

    def tlsa_rr_name_host(self):
        return "_" + str(self.port) + "." + \
               "_" + self.tlsa_protocol + "." + \
               self.host

    def tlsa_rr_name_fqdn(self):
        return "_" + str(self.port) + "." + \
               "_" + self.tlsa_protocol + "." + \
               self.fqdn + "."

    def tlsa_rr(self):
        return self.tlsa_rr_name_host() + \
               " IN TLSA " + \
               self.tlsa_rdata_3_1_1()

    def tlsa_rr_fqdn(self):
        return self.tlsa_rr_name_fqdn() + \
               " IN TLSA " + \
               self.tlsa_rdata_3_1_1()

    def connect(self):
        if self.probe_protocol == DANETLSAprotocols.DANETLSA_TLS:
            self.cert_pem = ssl.get_server_certificate((self.fqdn, self.port))
            self.cert_der = ssl.PEM_cert_to_DER_cert(self.cert_pem)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_SMTP:
            smtp = smtplib.SMTP(self.fqdn, port=self.port)
            smtp.starttls()
            self.cert_der = smtp.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_IMAP:
            imap = imaplib.IMAP4(self.fqdn, self.port)
            imap.starttls()
            self.cert_der = imap.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_POP3:
            pop = poplib.POP3(self.fqdn, self.port)
            pop.stls()
            self.cert_der = pop.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_PEM:
            f = open(self.certfile, "r")
            self.cert_pem = f.read()
            self.cert_der = ssl.PEM_cert_to_DER_cert(self.cert_pem)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_DER:
            f = open(self.certfile, "rb")
            self.cert_der = f.read()
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSAprotocols.DANETLSA_FTP:
            ftps = ftplib.FTP_TLS(self.fqdn)
            ftps.auth()
            self.cert_der = ftps.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        ### Parsing into X.509 object
        self.x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, self.cert_der)
