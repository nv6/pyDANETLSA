#!/usr/bin/env python3

from pyDANETLSA import DANETLSAprotocols, DANETLSA
from pyDANETLSA import DANETLSA_get_supported_protocols, DANETLS_protocol_to_str



def execute_test(fqdn=None, port=None, domain=None, transport_proto='tcp',
                 app_protocol=None, certfile=None):
    print("===")
    print("- input:")
    print("t fqdn           :", fqdn)
    print("t port           :", port)
    print("t domain         :", domain)
    print("t transport_proto  :", transport_proto)
    print("t app_protocol : {}({})".format(DANETLS_protocol_to_str(app_protocol), app_protocol))


    print("- run:")
    d = DANETLSA(fqdn=fqdn, port=port,
                            transport_proto=transport_proto,
                            app_protocol=app_protocol, certfile=certfile)

    print("i FQDN           :", d.fqdn)
    print("i Host           :", d.host)
    print("i Domain         :", d.domain)
    d.connect()

    print("- output:")
    print("Subject DN       :", d.subject_dn())
    print("Not valid after  :", d.x509_not_valid_after())
    print("Pub key hex      :", d.pubkey_hex())
    print("TLSA RR name/host:", d.tlsa_rr_name_host())
    print("TLSA RR name/host:", d.tlsa_rr_name_fqdn())
    print("TLSA rdata 3 1 1 :", d.tlsa_rdata_3_1_1())
    print("TLSA RR          :", d.tlsa_rr())
    print("TLSA RR with FQDN:", d.tlsa_rr_fqdn())
    print("DNS              :", d.dns_tlsa())
    print("Match DNS w/ X509:", d.match_cert_with_tlsa_rr())

    print("-- done.")


def runtest():
    try:
        # Expected to fail and raise an exception
        execute_test(fqdn='foobar.koeroo.net.', port=777, app_protocol=DANETLSAprotocols.DANETLSA_TLS,
                    certfile="dont_exists.pem")
    except Exception as e:
        print(e)

    try:
        execute_test(fqdn='foobar.koeroo.net.', port=777, app_protocol=DANETLSAprotocols.DANETLSA_PEM,
                    certfile="testcert/dummy.pem")
    except Exception as e:
        print(e)

    try:
        execute_test(fqdn='foobar.koeroo.net.', port=777, app_protocol=DANETLSAprotocols.DANETLSA_DER,
                    certfile="testcert/dummy.der")
    except Exception as e:
        print(e)


    execute_test(fqdn='smtp.koeroo.net',    port=25,  app_protocol=DANETLSAprotocols.DANETLSA_SMTP)
    execute_test(fqdn='mx.ncsc.nl',         port=25,  app_protocol=DANETLSAprotocols.DANETLSA_SMTP)
    execute_test(fqdn='mail.koeroo.net.',   port=143, app_protocol=DANETLSAprotocols.DANETLSA_IMAP)
    execute_test(fqdn='mail.koeroo.net.',   port=465, app_protocol=DANETLSAprotocols.DANETLSA_TLS)
    execute_test(fqdn='pop.kpnmail.nl',     port=110, app_protocol=DANETLSAprotocols.DANETLSA_POP3)

    execute_test(fqdn='test.rebex.net.',     port=21, app_protocol=DANETLSAprotocols.DANETLSA_FTP)


# MAIN
if __name__ == "__main__":
    runtest()

