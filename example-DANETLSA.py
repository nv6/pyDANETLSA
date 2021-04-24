#!/usr/bin/env python3

from src import pyDANETLSA

print("Protocol support list:", pyDANETLSA.DANETLS_protocols)


def execute_test(fqdn=None, port=None, domain=None, protocol=None, certfile=None):
    d = pyDANETLSA.danetlsa(fqdn=fqdn, port=port, protocol=protocol, certfile=certfile)
    print("FQDN:", d.fqdn)
    print("Host:", d.host)
    print("Domain:", d.domain)

    d.connect()
    print("Subject DN:", d.subject_dn())
    print("Pub key hex:", d.process_pubkey_hex())
    print("TLSA RR name/host:", d.tlsa_rr_name_host())
    print("TLSA rdata 3 1 1:", d.tlsa_rdata_3_1_1())
    print("TLSA RR:", d.tlsa_rr())
    print("TLSA RR with FQDN", d.tlsa_rr_fqdn())


try:
    # Expected to fail and raise an exception
    execute_test(fqdn='foobar.koeroo.net.', port=777, protocol=pyDANETLSA.DANETLSA_PEM,
                 certfile="dont_exists.pem")
except Exception as e:
    print(e)

execute_test(fqdn='foobar.koeroo.net.', port=777, protocol=pyDANETLSA.DANETLSA_PEM,
             certfile="dummy.pem")

execute_test(fqdn='smtp.koeroo.net.',   port=25,  protocol=pyDANETLSA.DANETLSA_SMTP)
execute_test(fqdn='smtp.koeroo.net.',   port=143, protocol=pyDANETLSA.DANETLSA_IMAP)
execute_test(fqdn='smtp.koeroo.net.',   port=465, protocol=pyDANETLSA.DANETLSA_TLS)
execute_test(fqdn='pop.kpnmail.nl',     port=110, protocol=pyDANETLSA.DANETLSA_POP3)

