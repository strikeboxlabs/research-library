# Inspect explicit FTPS without logging in

For FTP that upgrades its control connection, define `endpoint` as the authorized host/IP and port, `ftp_host` as its expected TLS hostname, and `ca_bundle` as independently trusted CA certificates. Define `transcript` as a fresh private file. This handshake sends no account credentials:

~~~bash
openssl s_client -connect "$endpoint" -starttls ftp -servername "$ftp_host" \
  -verify_hostname "$ftp_host" -verify_return_error -CAfile "$ca_bundle" \
  -showcerts </dev/null >"$transcript" 2>&1
status=$?
~~~

Use a harness deadline if the peer stalls. `-starttls ftp` performs the FTP upgrade exchange; omit it only for an endpoint already confirmed to use implicit TLS. SNI, hostname verification and chain verification serve different purposes. Retain exit status and verification diagnostics; default diagnostic s_client can continue after verification errors, so a negotiated cipher or `verify return:1` alone is not proof of trust.

For a self-signed/private-CA failure, obtain the expected CA/certificate through an independent trusted channel rather than turning the certificate just received into a trust anchor. If only the presented identity was acquired, report it as unverified and stop before credentials.

Extract a selected PEM certificate into a fresh `cert` file and inspect it with `openssl x509 -in "$cert" -noout -text -fingerprint -sha256`. SANs, subject CN and an email address in the subject are different fields. Names can guide separately scoped verification; they do not establish DNS existence, reachable virtual hosts or authorization to access them. `-showcerts` prints what the peer supplied, not necessarily a complete verified chain.

A successful control-channel handshake does not test FTP login, passive data connections or transfer protection. Use a TLS-capable FTP client such as lftp for the requested file operation, preserving its trust policy.

See [s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/) and [FTP TLS negotiation](https://www.rfc-editor.org/rfc/rfc4217.html).
