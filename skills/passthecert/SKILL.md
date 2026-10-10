---
name: passthecert
description: Authenticate to LDAP with a certificate using the Python PassTheCert CLI and manage a selected resource-based delegation entry. Use to distinguish Schannel mapping from PKINIT and certificate authentication from directory-write permission.
---

# Establish the mapped LDAP identity

Read this entire file before acting. Read [selected delegation changes](references/delegation-changes.md) fully before writing RBCD. Finish with the mapped identity, selected DC/object and verified result; a certificate filename or SAN is not proof of the server's account mapping.

Set `script` to the installed `Python/passthecert.py`, `cert_file` and `key_file` to a matching PEM certificate/private-key pair, and define `domain`, `dc_fqdn` and `dc_ip`. Inspect `python3 "$script" -h`. This package covers the Python LDAP client, not the separate Windows implementation.

~~~bash
ptc=(python3 "$script" -crt "$cert_file" -key "$key_file" -domain "$domain" \
  -dc-host "$dc_fqdn" -dc-ip "$dc_ip" -port 636)
"${ptc[@]}" -action whoami
~~~

Port 636 selects LDAPS; supported builds use StartTLS on 389. Keep transport protection and the correct DC identity. Certificate trust, validity, private-key access, supported authentication usage and the domain's mapping policy all affect the bind. A failed PKINIT attempt does not prove Schannel will work; test this protocol's result separately.

The private key remains sensitive after authentication. Do not place its passphrase or bytes in evidence. If the source artifact is PFX, obtain the required PEM pair through the installed certificate tooling and the task's protected-storage process; the PFX itself is not this CLI's `-crt` input.

Successful `whoami` establishes a mapped identity for this connection. It does not establish authority to modify another object's delegation descriptor. Inspect the actual action response and read back the affected object. See [upstream Python usage](https://github.com/AlmondOffSec/PassTheCert/tree/main/Python) for available actions and dependencies.
