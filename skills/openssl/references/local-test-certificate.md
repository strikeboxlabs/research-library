# Create a local test certificate

Require the owned local service and private output directory. Define `key` and `cert` as fresh paths; reject existing files before running. With OpenSSL3 and confirmed req options:

~~~bash
(
  umask 077 || exit
  openssl req -x509 -newkey rsa:2048 -sha256 -days 7 -noenc \
    -subj '/CN=localhost' -addext 'subjectAltName=DNS:localhost,IP:127.0.0.1' \
    -addext 'basicConstraints=critical,CA:FALSE' -keyout "$key" -out "$cert"
)
status=$?
~~~

This creates an unencrypted private key and self-signed certificate for the illustrative localhost names and seven-day lifetime. Preserve private permissions; deployment's key-loading and identity policy remain separate. Older versions may require their documented nodes/config-file equivalents instead of noenc/addext. Do not silently drop SANs.

Check status and parse the actual outputs:

~~~bash
openssl pkey -in "$key" -check -noout
openssl x509 -in "$cert" -noout -subject -issuer -dates -ext subjectAltName
~~~

Inspect the certificate public key against the private key's public component when association matters. Generation/parse does not establish browser trust or production issuance. Configure only the intended local test service and verify its actual presented certificate separately.

Source: [OpenSSL req](https://docs.openssl.org/3.5/man1/openssl-req/).
