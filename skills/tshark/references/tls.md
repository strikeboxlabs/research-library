# Diagnose TLS decryption from a saved capture

Use an existing approved capture; this procedure does not create traffic or obtain keys. Define `pcap` as its absolute path and `handshake_report` as a fresh private destination:

~~~bash
umask 077
tshark -n -r "$pcap" -Y 'tls.handshake' -V >"$handshake_report"
~~~

Inspect the selected ServerHello version/cipher, not just the TLS record-layer version or the certificate's signature algorithm. An RSA certificate can authenticate an ephemeral (EC)DHE exchange without enabling decryption by that certificate's private key. Record the TCP stream and whether the handshake is complete. For a verified TLS service on an observed nonstandard `port`, add `-d "tcp.port==$port,tls"`; a wrong protocol guess is not a missing-key diagnosis.

Choose the secret input that actually matches the captured session:

- An existing session key log can support modern TLS, including TLS 1.3 and (EC)DHE. Define `keylog` as its protected absolute path and set `secret_option="tls.keylog_file:$keylog"`. Secrets for a different connection do not help; enabling logging later cannot recover earlier uncaptured secrets.
- A server RSA private key works only for compatible RSA key exchange in TLS through 1.2, with the matching server certificate and the required non-resumed handshake, including ClientKeyExchange. Define `rsa_key` as a protected, unencrypted PEM key path without double quotes, backslashes or newlines, then set `secret_option="uat:rsa_keys:\"$rsa_key\",\"\""`. This uses the modern RSA key table; support depends on the build's crypto facilities. An encrypted key needs an appropriately protected preconfigured profile, not a passphrase pasted into the command line.

For a selected HTTP/1 investigation, define `requests` as a fresh private output:

~~~bash
tshark -n -2 -r "$pcap" -o "$secret_option" \
  -Y 'http.request || http.response' \
  -T fields -E header=y -E separator=/t -E quote=d \
  -e frame.number -e tcp.stream -e http.request.method \
  -e http.host -e http.request.uri -e http.response.code >"$requests"
~~~

`-2` performs two-pass analysis of the seekable capture. Check stderr/exit status and inspect the chosen stream: an unrelated plaintext HTTP request elsewhere in the capture is not evidence that the TLS stream decrypted. HTTP/2 needs its own dissector/fields, so an empty HTTP/1 table is inconclusive. Also check missing segments, truncated packets, TCP/TLS reassembly preferences, wrong key/session mapping and unsupported crypto before reporting a negative result.

Once the relevant `stream` is identified, define `transcript` as a new private file and inspect its decrypted application bytes:

~~~bash
tshark -n -r "$pcap" -o "$secret_option" \
  -q -z "follow,tls,ascii,$stream" >"$transcript"
~~~

This TLS follow selector uses the TCP stream index for that capture. Following TCP instead shows the underlying encrypted records. ASCII output is a reading aid, not a lossless binary export. A form submission reveals submitted values at capture time; correlate the server response and session state before claiming login success. Redact credentials in any resulting report.

Do not expect `-w` to produce a plaintext HTTP capture: it writes packet records, not this decoded text. A capture may already contain decryption-secret blocks, and TLS debug logs can contain secrets; both affect sharing and interpretation of an apparent no-key success. Keep secret material separate from ordinary reports.

Use the [TLS prerequisite guide](https://wiki.wireshark.org/TLS), [TShark options](https://www.wireshark.org/docs/man-pages/tshark.html) and [upstream decryption examples](https://github.com/wireshark/wireshark/blob/master/test/suite_decryption.py) to resolve build, preference and protocol differences.
