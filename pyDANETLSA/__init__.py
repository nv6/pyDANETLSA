import sys
import ssl
import imaplib
import poplib
import smtplib
import OpenSSL.crypto as crypto
import hashlib


DANETLSA_IMAP = 10
DANETLSA_POP3 = 20
DANETLSA_SMTP = 30
DANETLSA_TLS  = 40

DANETLS_protocols = [DANETLSA_IMAP, DANETLSA_POP3, DANETLSA_SMTP, DANETLSA_TLS]


class danetlsa(object):

    """
    IMAP: StartTLS for IMAP
    POP3: StartTLS for POP3
    SMTP: StartTLS for SMTP
    TLS: Plain TLS protocol, any application protocol
    """
    def __init__(self, host=None, port=None, protocol=DANETLSA_TLS):
        if protocol not in DANETLS_protocols:
            print("Error: unknown protocol set")
            return None

        if host is None:
            print("Error: no host")
            return None

        if port is None:
            print("Error: no port")
            return None

        self.host = host
        self.port = port
        self.protocol = protocol

    def subject_dn(self):
        """
        Output in OpenSSL format
        """
        s = ""
        for name, value in self.x509.get_subject().get_components():
            s = s + '/' + name.decode("utf-8") + '=' + value.decode("utf-8")

        return s

    def pubkey_hex(self):
        pubkey = crypto.dump_publickey(crypto.FILETYPE_ASN1, self.x509.get_pubkey())
        m = hashlib.sha256()
        m.update(pubkey)
        m.digest()
        return m.hexdigest()

    def connect(self):
        if self.protocol == DANETLSA_TLS:
            self.cert_pem = ssl.get_server_certificate((self.host, self.port))
            self.cert_der = ssl.PEM_cert_to_DER_cert(self.cert_pem)

        elif self.protocol == DANETLSA_SMTP:
            smtp = smtplib.SMTP(self.host, port=self.port)
            smtp.starttls()
            self.cert_der = smtp.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.protocol == DANETLSA_IMAP:
            imap = imaplib.IMAP4(self.host, self.port)
            imap.starttls()
            self.cert_der = imap.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        elif self.protocol == DANETLSA_POP3:
            pop = poplib.POP3(self.host, self.port)
            pop.stls()
            self.cert_der = pop.sock.getpeercert(binary_form=True)
            self.cert_pem = ssl.DER_cert_to_PEM_cert(self.cert_der)

        ### Parsing into X.509 object
        self.x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, self.cert_der)

