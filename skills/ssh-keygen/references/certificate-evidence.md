# Inspect an issued SSH certificate

Require the preserved certificate, intended user/host purpose and expected public key. Define `certificate` as its absolute working-copy path:

~~~bash
ssh-keygen -L -f "$certificate"
ssh-keygen -l -E sha256 -f "$certificate"
~~~

Retain status and the parsed type, public-key fingerprint, signing-CA fingerprint, serial, key ID, validity, principals, critical options and extensions. Compare the underlying public identity and signing CA with independently obtained public evidence; do not infer trust from a filename or comment. A parse failure leaves certificate interpretation incomplete.

The key ID is an issuance label, distinct from authorized principals and the requested OS account. A user certificate and host certificate serve different authentication directions. Check validity against the relevant clock; an unbounded validity interval is an observed issuance choice, not an operational requirement. Parsing does not prove current server acceptance or revocation status.

Finish with the artifact's supported identity and restrictions, plus any missing trust, clock or deployed-policy evidence. Issuing a replacement is a separate action, not a diagnostic fix for this artifact.

Reference: [ssh-keygen certificate inspection](https://man.openbsd.org/ssh-keygen.1).
