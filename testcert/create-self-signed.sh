#!/bin/bash

openssl req -x509 \
    -subj "/C=NL/O=MockTest/CN=foobar" \
    -nodes \
    -keyout dummy.key \
    -out dummy.pem \
    -days 3650

