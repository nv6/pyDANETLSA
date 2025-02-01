#!/usr/bin/env python3

import OpenSSL.crypto as crypto
import hashlib
import requests
import datetime

import ssl
#import socket
#from cryptography import x509
#from cryptography.x509.oid import ExtensionOID
#from cryptography.hazmat.primitives import hashes, serialization


def x509_to_subject_dn(cert):
    """
    Output in OpenSSL format
    """
    s = ""
    for name, value in cert.get_subject().get_components():
        s = s + '/' + name.decode("utf-8") + '=' + value.decode("utf-8")

    return s


def x509_to_pubkey_key(cert):
    pubkey = crypto.dump_publickey(crypto.FILETYPE_ASN1, cert.get_pubkey())
    m = hashlib.sha256()
    m.update(pubkey)
    m.digest()
    return m.hexdigest()

def time_left_on_certificate(cert):
    dt = datetime.datetime.strptime(cert.get_notAfter().decode("utf-8"), '%Y%m%d%H%M%SZ')
    now = datetime.datetime.now()
    delta = dt - now
    return delta

def x509_not_valid_after(cert):
    dt = datetime.datetime.strptime(cert.get_notAfter().decode("utf-8"), '%Y%m%d%H%M%SZ')
    return dt.isoformat()

def x509_not_valid_before(cert):
    dt = datetime.datetime.strptime(cert.get_notBefore().decode("utf-8"), '%Y%m%d%H%M%SZ')
    return dt.isoformat()


#def x509_extract_uri(cert):


def getCertificateFromUri(__uri):
    """Gets the certificate from a URI.
    By default, we're expecting to find nothing. Therefore certI = None. 
    If we find something, we'll update certI accordingly.
    """
    cert = None

    # Attempt to get the aia from __uri
    aiaRequest = requests.get(__uri)
    
    # If response status code is 200
    if aiaRequest.status_code == 200:
        # Get the content and assign to aiaContent
        aiaContent = aiaRequest.content

        # Convert the certificate into PEM format.
        sslCertificate = ssl.DER_cert_to_PEM_cert(aiaContent)

        # Load the PEM formatted content using x509 module.
        cert = x509.load_pem_x509_certificate(sslCertificate.encode('ascii'))

    # Return certI back to the script.
    return cert


def returnCertAKI(__sslCertificate):
    """Returns the AKI of the certificate."""
    try:
        certAKI = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_KEY_IDENTIFIER)
    except x509.extensions.ExtensionNotFound:
        certAKI = None
    return certAKI


def returnCertSKI(__sslCertificate):
    """Returns the SKI of the certificate."""
    certSKI = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)

    return certSKI


def returnCertAIA(__sslCertificate):
    """Returns the AIA of the certificate. If not defined, then return None."""
    try:
        certAIA = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS)

    except x509.extensions.ExtensionNotFound:
        certAIA = None
    
    return certAIA


def returnCertAIAList(__sslCertificate):
    """Returns a list of AIA's defined in __sslCertificate."""
    aiaUriList = []

    # Iterate through all the extensions.
    for extension in __sslCertificate.extensions:
        certValue = extension.value

        # If the extension is x509.AuthorityInformationAccess) then lets get the caIssuers from the field.
        if isinstance(certValue, x509.AuthorityInformationAccess):
            dataAIA = [x for x in certValue or []]
            for item in dataAIA:
                if item.access_method._name == "caIssuers":
                    aiaUriList.append(item.access_location._value)

    # Return the aiaUriList back to the script.
    return aiaUriList


def walkTheChain(__sslCertificate, __depth):
    """
    Walk the length of the chain, fetching information from AIA 
    along the way until AKI == SKI (i.e. we've found the Root CA.

    This is to prevent recursive loops. Usually there are only 4 certificates. 
    If the maxDepth is too small (why?) adjust it at the beginning of the script.
    """
    if __depth <= maxDepth:
        # Retrive the AKI from the certificate.
        certAKI = returnCertAKI(__sslCertificate)
        # Retrieve the SKI from the certificate.
        certSKI = returnCertSKI(__sslCertificate)

        # Sometimes the AKI can be none. Lets handle this accordingly.
        if certAKI is not None:
            certAKIValue = certAKI._value.key_identifier
        else:
            certAKIValue = None

        # Get the value of the SKI from certSKI
        certSKIValue = certSKI._value.digest
        
        # Sometimes the AKI can be none. Lets handle this accordingly.
        if certAKIValue is not None:
            aiaUriList = returnCertAIAList(__sslCertificate)
            if aiaUriList != []:
                # Iterate through the aiaUriList list.
                for item in aiaUriList:
                    # get the certificate for the item element.
                    nextCert = getCertificateFromUri(item)

                    # If the certificate is not none (great), append it to the certChain, increase the __depth and run the walkTheChain subroutine again.
                    if nextCert is not None:
                        certChain.append(nextCert)
                        __depth += 1
                        walkTheChain(nextCert, __depth)
                    else:
                        print("Could not retrieve certificate.")
                        sys.exit(1)
            else:
                """Now we have to go on a hunt to find the root from a standard root store."""
                print("Certificate didn't have AIA...ruh roh.")
