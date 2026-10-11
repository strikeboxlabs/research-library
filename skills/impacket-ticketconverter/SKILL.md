---
name: impacket-ticketconverter
description: Convert a known owned single-ticket Kerberos artifact offline between KRB-CRED kirbi and FILE credential-cache formats. Use when an application needs a different container format, while checking metadata, truncation and multi-ticket loss.
---

# Convert an owned Kerberos file offline

Read this entire SKILL.md before acting. Require the installed Impacket ticketConverter implementation, a complete known owned artifact and a fresh private output path. Confirm this is a supported single-ticket conversion. Complete with converter status, output format and ticket-metadata checks, or an explicit parsing/coverage gap. Conversion does not authenticate to a service.

The commonly packaged command is case-sensitive `impacket-ticketConverter`; upstream supplies `ticketConverter.py`. Select the installed wrapper rather than guessing its path. Set `input_file` and `output_file` to distinct real paths in an owned directory, with the intended opposite format:

~~~bash
umask 077
test -s "$input_file"
test ! -e "$output_file" && test ! -L "$output_file"
impacket-ticketConverter "$input_file" "$output_file"
~~~

Only proceed after both checks succeed. The output contains authentication material and the implementation overwrites its destination. Keep the input intact. Raw binary KRB-CRED is required for kirbi input; a base64 string, truncated `<SNIP>` transcript or terminal screenshot is not that file.

Impacket 0.12.0 chooses direction from the first byte: `0x76` for KRB-CRED and `0x05` for ccache. This is only a discriminator, not complete validation. Empty or malformed input can raise an exception; `unknown file format` can finish without an error exit. Require the expected new nonempty artifact and successful parse, rather than trusting status alone.

The reviewed 0.12.0 CCache conversion uses the first ticket/credential only. It also expects a supported unencrypted KRB-CRED ticket-info representation and service-principal shape. Do not use it to preserve a multi-ticket cache or promise a byte-for-byte reversible archival transformation. Confirm installed-version behavior before expanding that scope.

For a converted FILE cache, inspect its metadata offline with MIT `klist`, if available:

~~~bash
klist -c "$output_file"
~~~

Compare expected client, realm, service principal, validity times and ticket count with the input's known metadata. An expired ticket stays expired; a wrong service principal stays wrong. A conversion-success message does not repair an SPN, renew credentials, change account membership or prove service authorization. If an independent parser is unavailable, report that validation gap rather than claiming a successful login.

Primary implementation: [Impacket ticketConverter](https://github.com/fortra/impacket/blob/impacket_0_12_0/examples/ticketConverter.py) and [CCache conversion methods](https://github.com/fortra/impacket/blob/impacket_0_12_0/impacket/krb5/ccache.py). See the [MIT FILE cache format](https://web.mit.edu/kerberos/krb5-latest/doc/formats/ccache_file_format.html) for container interpretation.
