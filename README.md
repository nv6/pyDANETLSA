Author: Oscar Koeroo


# pyDANETLSA
Generate TLSA record for DANE. Generated either by probing the resource and using a StartTLS or plain TLS handshake to extract the certificate, public key and formulate a TLSA 3 1 1 format. Also a X.509 in PEM or DER file format is possible.

## Class: danetlsa
### Initializer / __init__():
Start a new instance of pyDANETLSA and initialize it with the following named attributes:
* fqdn: Fully Qualified Domain Name which sets the full name of a host, e.g. smtp.koeroo.net. From this value the domain and host part is extracted. However, the algorithm expects a zone of two components, being the TLD and the zone name. If this is either three or one for gTLDs the calculation is borked. Use the '''domain''' attribute to force the calculation to become relative to the provided domain instead of guessing the zone structure.
* port: The TCP or UDP port number for with the DANE TLSA record is to be generated.
* protocol: Selects the probe method/read method. Choices are fixed to:
    10. DANETLSA_IMAP: Probes IMAP with StartTLS on the provided port.
    20. DANETLSA_POP3: Probes POP3 with StartTLS on the provided port.
    30. DANETLSA_SMTP: Probes SMTP with StartTLS on the provided port.
    40. DANETLSA_TLS: Probes with plain TLS on the provided port.
    50. DANETLSA_PEM: Reads a certificate from the '''certfile''' property. The file must be in PEM format.
    60. DANETLSA_DER: Reads a certificate from the '''certfile''' property. The file must be in DER format.
* certfile: Optional for network probe '''protocol''' selections. File path to a PEM or DER certificate to read. File must exist and must be a file (or symlink to a file).

### connect()
See '''engage()'''

### engage()
This will trigger the reading of the file or start the network connection to the selected '''protocol''' to extract the certificate, transform the certificate in the right internal formats and generate the information required for a DANE TLSA record. This information can then be retried with other methods.

### subject_dn()
Returns the Subject DN in classic OpenSSL subject format.
```
/C=NL/ST=Zuid-Holland/L='s-Gravenhage/O=Rijksoverheid/CN=ncsc.nl
```

### process_pubkey_hex()
Internal function to process the public key hex value from the fetched certificate.
Returns the hex value
```
78a80c6362af724f11433375890632cc099cd55a985c6e4a4a8ad741fe032f35
```

### pubkey_hex()
Returns the hex value of the public key.
```
78a80c6362af724f11433375890632cc099cd55a985c6e4a4a8ad741fe032f35
```

### tlsa_rdata_3_1_1()
Returns the '''3 1 1''' format value.
```
3 1 1 78a80c6362af724f11433375890632cc099cd55a985c6e4a4a8ad741fe032f35
```

### tlsa_rr_name_host()
Returns the resource record name for TLSA appropriate for the service.
```
_25._tcp.smtp
```

### tlsa_rr_name_fqdn()
Returns the resource record name as full FQDN value for TLSA appropriate for the service.
```
_25._tcp.smtp.koeroo.net.
```

### tlsa_rr()
Returns full resource record, which looks a lot like a zone file.
```
_25._tcp.smtp IN TLSA 3 1 1 78a80c6362af724f11433375890632cc099cd55a985c6e4a4a8ad741fe032f35
```

### tlsa_rr_fqdn()
Returns full resource record, which looks a lot like a zone file, the host is now an absolute name.
```
_465._tcp.smtp.koeroo.net. IN TLSA 3 1 1 78a80c6362af724f11433375890632cc099cd55a985c6e4a4a8ad741fe032f35
```


## Example:
```python
#!/usr/bin/env python3

import pyDANETLSA

print("Protocol support list:", pyDANETLSA.DANETLS_protocols)

d = pyDANETLSA.danetlsa(fqdn='smtp.koeroo.net.', port=25,  protocol=pyDANETLSA.DANETLSA_SMTP)
d.connect()
print("TLSA RR with FQDN", d.tlsa_rr_fqdn())
```

