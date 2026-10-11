# Inspect ASN.1 structure without claiming verification

Define `object` as a complete acquired raw artifact and establish its expected DER/PEM encoding. For a DER object:

~~~bash
openssl asn1parse -inform DER -in "$object" -i
~~~

Retain status and diagnostics. The offsets refer to the supplied input, while depth, header length, content length and tag describe nested structure. A parsed prefix is insufficient when trailing bytes or a length error remain. A raw section may contain a certificate, a signed container, unrelated ASN.1 or multiple objects; identify the format before choosing another decoder.

`asn1parse` is a structural diagnostic, not signature verification. Finding an organization string or a BIT/OCTET STRING does not bind it to an executable's code bytes or trusted issuer. A signature assessment needs the defined signed bytes, algorithms, matching public key and trust policy. Preserve that distinction when reviewing a checker that greps parser output. Do not recreate or modify a signature-bearing artifact merely to test a metadata finding.

See the [ASN.1 parser manual](https://docs.openssl.org/3.5/man1/openssl-asn1parse/) for format, offsets and nested parsing.
