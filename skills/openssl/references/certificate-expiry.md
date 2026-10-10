# Distinguish approaching expiry from a failed check

For an existing PEM `cert` and a nonnegative integer `seconds` defining the renewal horizon, first require successful parsing and retain the dates:

~~~bash
if openssl x509 -in "$cert" -noout -dates -subject; then
    if openssl x509 -in "$cert" -noout -checkend "$seconds"; then
        printf 'Certificate expiry is beyond the selected horizon.\n'
    else
        printf 'Nonzero check: inspect expiry result and diagnostics.\n'
    fi
else
    printf 'Certificate could not be inspected; expiry is unresolved.\n' >&2
fi
~~~

`-checkend 86400` asks whether `notAfter` falls within the next 86,400 seconds, relative to the checking host's clock. For a valid parsed certificate, zero means it does not expire within that horizon; nonzero is also possible for malformed/unreadable input or invocation errors. Do not route every failure into renewal. Keep the exact diagnostic and parsed `notAfter` together. The illustrative messages above are workflow labels, not captured OpenSSL output.

This checks expiry, not `notBefore`, chain trust, hostname or the service's currently loaded certificate. A one-day self-signed fixture soon falls inside a one-day horizon; it does not establish trusted issuance. Treat subject/CN strings as untrusted data when passing them to a renewal script or constructing filenames. Certificate parsing does not itself execute shell syntax embedded in a name.

For certificate-based login, confirm the matching private key exists and is readable by the intended process without printing it. Record certificate fingerprints and verification diagnostics, not private-key contents.

Resolve certificate-option differences with the [request](https://docs.openssl.org/3.5/man1/openssl-req/), [certificate](https://docs.openssl.org/3.5/man1/openssl-x509/) and [verification](https://docs.openssl.org/3.5/man1/openssl-verify/) manuals.
