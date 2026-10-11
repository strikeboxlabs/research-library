---
name: wireshark
description: Review a saved local packet capture in the Wireshark GUI with packet-tree and conversation context. Use when broad filters, adjacent authentication protocols or nested Kerberos fields support a misleading interpretation.
---

# Inspect saved protocol evidence

Read this entire SKILL.md before acting. Require an existing authorized capture, trusted installed analyzer and usable graphical session. Keep the original capture and selected frame/conversation identity; finish with observed protocol/field evidence and capture limits. No conditional resources are required.

Define `wireshark_bin` as the installed executable and `capture` as the absolute path to the selected local pcap/pcapng. Launch saved-file review without starting live capture:

~~~bash
"$wireshark_bin" --version
"$wireshark_bin" -n -r "$capture" -Y 'kerberos || ntlmssp'
~~~

`-r` reads the capture; `-n` disables name resolution. `-Y` is a display filter, distinct from the capture-filter syntax of `-f`. The filter hides other packets, rather than proving the capture contains only authentication. Inspect total/displayed counts and file/dissection diagnostics; clear or narrow the display filter to review surrounding requests/replies. No match can reflect missing packets, disabled dissectors, encapsulation or an analyzer-version issue.

Select a frame and expand its protocol tree. Retain frame number, capture time, source/destination, transport ports, conversation and the field's full parent hierarchy. **Illustrative:** neighboring SMB Session Setup/NTLMSSP and TCP port 88 Kerberos AS-REQ packets are separate exchanges; an AS-REQ is not NTLM authentication transmitted inside SMB merely because both appear under one filter. A packet's client principal is a capture-time claim, not proof of a completed login or present credentials.

For Kerberos, distinguish AS-REQ, AS-REP and KRB-ERROR. Within AS-REQ, PA-DATA type 2 is PA-ENC-TIMESTAMP: inspect that encrypted value's own encryption type separately from the request body's supported-encryption list. An initial request may use another pre-authentication method or omit the timestamp before a KDC response. Its ciphertext is not a plaintext password, NT hash or generic timestamp hash. Retain principal/realm association and relevant exchange context without converting or replaying secrets.

Check truncated frames, missing TCP segments and capture start/end before asserting completeness. Exported text/screenshots can omit fields or truncate bytes; preserve the original private capture and frame references. A GUI launch, valid display filter or selected decrypted field alone does not prove an application's authentication success. File analysis needs ordinary file access; do not elevate to root or start live capture to work around a GUI/session problem.

Use the [Wireshark CLI manual](https://www.wireshark.org/docs/man-pages/wireshark.html), [display-filter guide](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html), [Kerberos fields](https://www.wireshark.org/docs/dfref/k/kerberos.html) and [Kerberos exchange definitions](https://www.rfc-editor.org/rfc/rfc4120.html) to resolve version/field questions.
