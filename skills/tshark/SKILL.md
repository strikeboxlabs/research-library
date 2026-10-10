---
name: tshark
description: Analyze saved FTP, TLS or Kerberos traffic with frame and conversation context. Use when incomplete conversations, decryption prerequisites or filtered output could support a misleading application conclusion.
---

# Correlate evidence in a saved capture

Use `tshark --version` and `tshark -h` to establish the installed analyzer. Define `pcap` as the existing capture to inspect and `events` as a fresh private text output path. Reading with `-r` needs file access, not live-capture privileges; omitting it can start a capture.

Extract FTP login commands and server responses while retaining frame, time, endpoints and stream identity:

~~~bash
umask 077
tshark -n -r "$pcap" \
  -Y 'ftp.request.command == "USER" || ftp.request.command == "PASS" || ftp.response.code' \
  -T fields -E header=y -E separator=/t -E quote=d \
  -e frame.number -e frame.time_epoch -e tcp.stream \
  -e ip.src -e ipv6.src -e tcp.srcport \
  -e ip.dst -e ipv6.dst -e tcp.dstport \
  -e ftp.request.command -e ftp.request.arg \
  -e ftp.response.code -e ftp.response.arg >"$events"
~~~

`-Y` uses Wireshark display filters; `-f` uses capture-filter syntax. `-n` disables name resolution. The exported text can contain cleartext passwords. Keep it private and redact values when reporting the finding. `-w` writes packet data, so it is not a replacement for this text redirection. Preserve stderr and the exit status: invalid fields, unreadable files or dissection errors are not empty evidence.

Read each stream in frame order and match request/reply direction. **Illustrative:** `USER analyst`, a `331` reply, `PASS [redacted]` and a subsequent `230` in that conversation support an accepted login at capture time. `331` alone requests a password; `530` means not logged in. A visible PASS command proves disclosure of submitted bytes even without success. It does not establish their present validity or reuse on SSH or another service. Keep separate attempts within the same connection distinct.

## Inspect the surrounding conversation

Define `stream` as a nonnegative integer from the `tcp.stream` column and `transcript` as a fresh private destination:

~~~bash
tshark -n -r "$pcap" -q -z "follow,tcp,ascii,$stream" >"$transcript"
~~~

The stream selector applies to this capture; stream 0 is the first TCP stream, not frame 0 or a globally stable connection ID. Following reconstructs the available byte stream and preserves direction through its node labels and indentation. ASCII presentation replaces nonprintable bytes with dots, so use hex mode and the original capture when exact bytes matter.

A missing match can mean encrypted FTP, a nonstandard port, an incomplete capture or a dissector/configuration issue. Inspect endpoints and available TCP payload before asserting absence. For a verified plaintext FTP control service on an observed nonstandard `port`, add `-d "tcp.port==$port,ftp"`; forcing a dissector cannot decrypt TLS or validate an arbitrary protocol guess. Use `tshark -G fields` to resolve unavailable field names.

Check missing segments, retransmissions and truncated frames before treating a transcript as complete. An early `-c` limit counts packets read, including nonmatching packets, so it can hide later authentication without an obvious empty-file error. Preserve capture identity and frame/stream references in the conclusion; decrypted or reconstructed evidence still reflects only what the file contains.

For an existing TLS capture and authorized session secrets or a matching server key, use [TLS decryption and application evidence](references/tls.md).

See the [TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html), [FTP fields](https://www.wireshark.org/docs/dfref/f/ftp.html), [TCP analysis guide](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html) and [FTP reply definitions](https://www.rfc-editor.org/rfc/rfc959.html).


## Resolve a Kerberos pre-authentication exchange

For the existing `pcap`, define `summary` and `detail` as fresh private text files. Locate AS requests, AS replies and errors with their endpoints before selecting one packet:

~~~bash
umask 077
tshark -n -r "$pcap" \
  -Y 'kerberos.msg_type == 10 || kerberos.msg_type == 11 || kerberos.msg_type == 30' \
  -T fields -E header=y -E separator=/t -E quote=d -E occurrence=a \
  -e frame.number -e frame.time_epoch -e tcp.stream -e udp.stream \
  -e ip.src -e ipv6.src -e ip.dst -e ipv6.dst \
  -e kerberos.msg_type -e kerberos.CNameString -e kerberos.realm \
  -e kerberos.padata_type -e kerberos.error_code >"$summary"
~~~

Use endpoints, transport conversation, time and request/reply context together. Type 10 is AS-REQ, 11 AS-REP and 30 KRB-ERROR. An initial error 25 (`KDC_ERR_PREAUTH_REQUIRED`) can be the normal invitation to supply pre-authentication; it does not by itself mean a wrong password. An AS-REP supports a KDC response, not successful later SMB access.

Select `frame` as a numeric frame number from this capture. Preserve the decoded hierarchy:

~~~bash
tshark -n -r "$pcap" -Y "frame.number == $frame" -V >"$detail"
~~~

Within an AS-REQ, locate PA-DATA type 2, **PA-ENC-TIMESTAMP**, and its own encrypted-data `etype` and `cipher`. Keep these with the request body's client principal and realm. The request body's supported-encryption list is a different field from the encryption type of this timestamp. A flat export of every `kerberos.etype` or `kerberos.cipher` can mix unrelated nested values; selecting the first occurrence is not a reliable correction.

The timestamp ciphertext is neither a plaintext password, an NT hash nor an AS-REP record. If an offline audit needs a converted record, retain the complete capture, selected frame and relevant KDC salt/parameter evidence; use a converter appropriate to the actual encryption type. Do not substitute a DNS suffix for the observed realm or assume the default salt fits every principal. No matching type-2 field can reflect another pre-authentication method, a wrapped exchange, missing packets or dissection failure. Inspect the surrounding exchange before claiming no pre-authentication.

The [Kerberos field reference](https://www.wireshark.org/docs/dfref/k/kerberos.html) identifies case-sensitive field names and supported analyzer versions; [RFC 4120](https://www.rfc-editor.org/rfc/rfc4120.html) defines the exchange and encrypted timestamp. Treat an unavailable field error as an analyzer-version issue, not an empty capture.
