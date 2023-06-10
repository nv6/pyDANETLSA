#!/usr/bin/env python3

import sys
import os
import ssl
import ftplib
import imaplib
import poplib
import smtplib
import OpenSSL.crypto as crypto
import hashlib


DANETLSA_IMAP = 10
DANETLSA_POP3 = 20
DANETLSA_SMTP = 30
DANETLSA_TLS  = 40
DANETLSA_PEM  = 50
DANETLSA_DER  = 60
DANETLSA_FTP  = 70

DANETLS_protocols = [DANETLSA_IMAP, DANETLSA_POP3, DANETLSA_SMTP,
                     DANETLSA_TLS,  DANETLSA_PEM,  DANETLSA_DER,
                     DANETLSA_FTP]

def DANETLS_protocol_to_str(protocol):
    if protocol not in DANETLS_protocols:
        raise ValueError("Unknown protocol/method set")

    if   protocol == DANETLSA_IMAP: return "IMAP"
    elif protocol == DANETLSA_POP3: return "POP3"
    elif protocol == DANETLSA_SMTP: return "SMTP"
    elif protocol == DANETLSA_TLS : return "TLS"
    elif protocol == DANETLSA_PEM : return "PEM"
    elif protocol == DANETLSA_DER : return "DER"
    elif protocol == DANETLSA_FTP : return "FTP"

class danetlsa(object):

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
                       tlsa_protocol='tcp', probe_protocol=DANETLSA_TLS,
                       certfile=None):
        if tlsa_protocol.lower() not in ['tcp', 'udp', 'sctp']:
            raise ValueError("Unknown protocol/method set for TLSA output record.")

        if probe_protocol not in DANETLS_protocols:
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

    def process_pubkey_hex(self):
        pubkey = crypto.dump_publickey(crypto.FILETYPE_ASN1, self.x509.get_pubkey())
        m = hashlib.sha256()
        m.update(pubkey)
        m.digest()
        self.pubkey_hex = m.hexdigest()
        return self.pubkey_hex

    def pubkey_hex(self):
        return self.pubkey_hex

    def subject_dn(self):
        """
        Output in OpenSSL format
        """
        s = ""
        for name, value in self.x509.get_subject().get_components():
            s = s + '/' + name.decode("utf-8") + '=' + value.decode("utf-8")

        return s

    def tlsa_rdata_3_1_1(self):
        return "3 1 1 " + self.pubkey_hex

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
        self.engage()

    def engage(self):
        if self.probe_protocol == DANETLSA_TLS:
            self.cert_pem = ssl.get_server_certificate((self.fqdn, self.port))
            self.cert_der = ssl.PEM_cert_to_DER_cert(self.cert_pem)

        elif self.probe_protocol == DANETLSA_SMTP:
            smtp = smtplib.SMTP(self.fqdn, port=self.port)
            smtp.starttls()
            self.cert_der = smtp.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSA_IMAP:
            imap = imaplib.IMAP4(self.fqdn, self.port)
            imap.starttls()
            self.cert_der = imap.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSA_POP3:
            pop = poplib.POP3(self.fqdn, self.port)
            pop.stls()
            self.cert_der = pop.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSA_PEM:
            f = open(self.certfile, "r")
            self.cert_pem = f.read()
            self.cert_der = ssl.PEM_cert_to_DER_cert(self.cert_pem)

        elif self.probe_protocol == DANETLSA_DER:
            f = open(self.certfile, "rb")
            self.cert_der = f.read()
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.probe_protocol == DANETLSA_FTP:
            ftps = ftplib.FTP_TLS(self.fqdn)
            ftps.auth()
            self.cert_der = ftps.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)


        ### Parsing into X.509 object
        self.x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, self.cert_der)

        ### Extrct public key and store the HEX value for it, conforming 3 1 1.
        self.process_pubkey_hex()

