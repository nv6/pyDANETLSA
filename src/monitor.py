#!/usr/bin/env python3

import os
import argparse

from pyDANETLSA import DANETLSAprotocols, DANETLSA
from pyDANETLSA import DANETLSA_get_supported_protocols, DANETLS_protocol_to_str, str_to_DANETLS_protocol

from libs.configuration import parse_config


print("Protocol support list:", DANETLSA_get_supported_protocols())


def execute_test(fqdn=None, port=None, domain=None, tlsa_protocol='tcp', 
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
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument("-f", "--fqdn",
                        dest='fqdn',
                        help="FQDN",
                        default=None,
                        type=str)
    parser.add_argument("-p", "--port",
                        dest='port',
                        help="Port number",
                        default=None,
                        type=str)
    parser.add_argument("-t", "--protocol",
                        dest='protocol',
                        help="Protocol",
                        default=None,
                        type=str)

    args = parser.parse_args()

    execute_test(fqdn=args.fqdn,
                 port=args.port,
                probe_protocol=str_to_DANETLS_protocol(args.protocol))
