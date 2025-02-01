#!/usr/bin/env python3


from pyDANETLSA import DANETLSA, DANETLSAprotocols


d = DANETLSA(fqdn='smtp.koeroo.net', port=25,
             app_protocol=DANETLSAprotocols.DANETLSA_SMTP)
d.connect()


print("- output:")
print("Subject DN       :", d.subject_dn())
print("TLSA RR host     :", d.tlsa_rr_name_host())
print("TLSA RR name     :", d.tlsa_rr_name_fqdn())
print("TLSA rdata 3 1 1 :", d.tlsa_rdata_3_1_1())
print("TLSA RR          :", d.tlsa_rr())
print("TLSA RR with FQDN:", d.tlsa_rr_fqdn())
print("DNS results      :", d.dns_tlsa())
print("Match DNS w/ X509:", d.match_cert_with_tlsa_rr())
print("-- done.")


# On match, True. Otherwise False
print(d.results_to_dict())
