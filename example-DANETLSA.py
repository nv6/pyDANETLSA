#!/usr/bin/env python3
import pyDANETLSA


# d = pyDANETLSA.danetlsa()

d = pyDANETLSA.danetlsa(fqdn='smtp.koeroo.net.', port=25, protocol=pyDANETLSA.DANETLSA_SMTP)
print(d.fqdn)
print(d.host)
print(d.domain)

d.connect()
print(d.subject_dn())
print(d.process_pubkey_hex())
print(d.tlsa_rr_name_host())
print(d.tlsa_rdata_3_1_1())
print(d.tlsa_rr())
print(d.tlsa_rr_fqdn())

d = pyDANETLSA.danetlsa(fqdn='smtp.koeroo.net.', port=143, protocol=pyDANETLSA.DANETLSA_IMAP)
print(d.fqdn)
print(d.host)
print(d.domain)

d.connect()
print(d.subject_dn())
print(d.process_pubkey_hex())
print(d.tlsa_rr_name_host())
print(d.tlsa_rdata_3_1_1())
print(d.tlsa_rr())
print(d.tlsa_rr_fqdn())

d = pyDANETLSA.danetlsa(fqdn='smtp.koeroo.net.', port=465, protocol=pyDANETLSA.DANETLSA_TLS)
print(d.fqdn)
print(d.host)
print(d.domain)

d.connect()
print(d.subject_dn())
print(d.process_pubkey_hex())
print(d.tlsa_rr_name_host())
print(d.tlsa_rdata_3_1_1())
print(d.tlsa_rr())
print(d.tlsa_rr_fqdn())

d = pyDANETLSA.danetlsa(fqdn='pop.kpnmail.nl', port=110, protocol=pyDANETLSA.DANETLSA_POP3)
print(d.fqdn)
print(d.host)
print(d.domain)

d.connect()
print(d.subject_dn())
print(d.process_pubkey_hex())
print(d.tlsa_rr_name_host())
print(d.tlsa_rdata_3_1_1())
print(d.tlsa_rr())
print(d.tlsa_rr_fqdn())
