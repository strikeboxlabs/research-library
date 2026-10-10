---
name: sslscan
description: Enumerate supported TLS protocols, cipher suites and certificate details on a scoped endpoint.
---

# sslscan TLS survey

Read this entire SKILL.md before acting. Define the authorized `host`, `port` and a fresh `output` path; identify the required SNI name and whether the service uses direct TLS or STARTTLS. This scan performs active handshakes and vulnerability checks. Finish with endpoint/SNI, scan completion, negotiated protocols and ciphers, certificate observations and unresolved errors.

## Installed implementation

Use `/usr/bin/sslscan`, version 2.1.5, linked against OpenSSL 3.6.4. `--no-colour` makes saved output readable. This version's help does not list the older `--no-failed` option; omit it. Certificate retrieval requires a successful handshake.

## Survey command

For direct TLS:

~~~bash
/usr/bin/sslscan --no-colour "$host:$port" > "$output" 2>&1
~~~

When connecting to an IP for a named virtual host, add `--sni-name "$sni"` with the intended DNS name. For an explicit upgrade protocol, select the matching option such as `--starttls-smtp` or `--starttls-imap`; probing a plaintext greeting as direct TLS does not test that service's STARTTLS configuration. Consult `/usr/bin/sslscan --help` for the installed protocol options.

## Reading the output

Illustrative protocol and cipher excerpt:

~~~text
TLSv1.0   disabled
TLSv1.1   disabled
TLSv1.2   enabled
TLSv1.3   enabled
Preferred TLSv1.3  128 bits  TLS_AES_128_GCM_SHA256
Accepted  TLSv1.3  256 bits  TLS_CHACHA20_POLY1305_SHA256
~~~

- An enabled protocol or accepted cipher reflects a successful probe from this client and vantage. Compare the observed set with the endpoint's required policy; do not infer complete security from modern protocol support alone.
- `Preferred` identifies a preference observed by the scanner; both `Preferred` and `Accepted` suites are supported. Judge a suite by its algorithms and parameters, not by the label or bit count alone.
- A negative Heartbleed result is limited to the completed probe. A missing result or failed handshake is not a negative test, and this check does not assess unrelated vulnerabilities.
- Certificate identity and chain output are observations. They do not by themselves establish trusted hostname validation by an application client.

If every protocol is reported disabled alongside connection or certificate-retrieval failures, no usable handshake was established. Check address/port, SNI, direct TLS versus STARTTLS, reachability and scan errors before concluding the service lacks TLS. A certificate parsing error remains unresolved until the returned certificate data and scanner behavior are inspected; it does not alone prove either a server fault or a scanner fault.
