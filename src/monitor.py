#!/usr/bin/env python3

import sys

from pyDANETLSA import DANETLSAprotocols, DANETLSA
from pyDANETLSA import DANETLS_protocol_to_str, str_to_DANETLS_protocol

from libs.configuration import arguments, is_startup_clean



def execute_test(fqdn=None, port=25, domain=None, 
                tlsa_protocol='tcp', 
                probe_protocol=None, certfile=None):
    print("===")
    print("- input:")
    print("t fqdn           :", fqdn)
    print("t port           :", port)
    print("t domain         :", domain)
    print("t tlsa_protocol  :", tlsa_protocol)
    print("t probe_protocol : {}({})".format(DANETLS_protocol_to_str(probe_protocol), probe_protocol))


    print("- run:")
    d = DANETLSA(fqdn=fqdn, port=port,
                            tlsa_protocol=tlsa_protocol,
                            probe_protocol=probe_protocol, certfile=certfile)

    print("i FQDN           :", d.fqdn)
    print("i Host           :", d.host)
    print("i Domain         :", d.domain)
    d.connect()

    print("- output:")
    print("Subject DN       :", d.subject_dn())
    print("Pub key hex      :", d.pubkey_hex())
    print("TLSA RR name/host:", d.tlsa_rr_name_host())
    print("TLSA RR name/host:", d.tlsa_rr_name_fqdn())
    print("TLSA rdata 3 1 1 :", d.tlsa_rdata_3_1_1())
    print("TLSA RR          :", d.tlsa_rr())
    print("TLSA RR with FQDN:", d.tlsa_rr_fqdn())
    print("DNS              :", d.dns_tlsa())
    print("Match DNS w/ X509:", d.match_cert_with_tlsa_rr())

    print("-- done.")



if __name__ == "__main__":
    args = arguments()
    if not is_startup_clean(args):
        sys.exit(1)

    if args.verbose:
        execute_test(fqdn=args.fqdn,
                    port=args.port,
                    tlsa_protocol=args.transport.lower(),
                    probe_protocol=str_to_DANETLS_protocol(args.protocol))

    else:
        d = DANETLSA(fqdn=args.fqdn, port=args.port,
                     tlsa_protocol=args.transport.lower(),
                     probe_protocol=str_to_DANETLS_protocol(args.protocol))
        d.connect()

        if d.match_cert_with_tlsa_rr():
            print("{ \"DANETLS_OK\":true }")
            sys.exit(0)
        else:
            print("{ \"DANETLS_OK\":false }")
            sys.exit(1)
