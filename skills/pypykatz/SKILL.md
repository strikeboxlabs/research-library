---
name: pypykatz
description: Inspect existing LSASS minidumps or derive a known-password NT value offline with pypykatz. Use to preserve session identity and distinguish NT keys, NetNTLMv2 responses and parsing failures.
---

# Inspect an existing LSASS minidump

Use an existing process minidump from the authorised acquisition. Preserve its hash, source machine and capture time; a filename such as `lsass.DMP` alone does not establish its process or format. Extract an archive into a separate working directory before selecting the actual dump. A full-system memory image requires a different reader.

Check `pypykatz lsa -h` for this release's input, package and output options. Define `dump` as the absolute working-copy filename, `report` as a fresh private JSON filename and `log` as a fresh diagnostic filename. For an MSV-focused inspection:

~~~bash
umask 077
pypykatz lsa minidump "$dump" --packages msv --json --outfile "$report" --halt-on-error >"$log" 2>&1
~~~

This parses local bytes; it neither acquires a live process nor authenticates to another machine. `--packages msv` limits package coverage. Choose additional packages only when the task needs their material; omitted packages cannot support a negative conclusion. `--halt-on-error` makes detected parsing failures stop the run. Check diagnostics, exit status and the newly written report together; a file's existence alone is insufficient.

Read the output's file/session structure before filtering it. Keep source file, session LUID/SID, domain, username and credential package attached to each record, including differing identities inside a session. Never independently sort usernames and hashes into separate files: that destroys their relationship. Retain orphaned credentials as unassociated unless another observation resolves them. JSON field names and byte representation should be checked against the installed release before scripting extraction.

**Illustrative findings and decisions:**

| Finding | Supported interpretation |
|---|---|
| A named session has an MSV NT value | Credential material was recoverable in this snapshot. It is not plaintext or proof of current login access. |
| A session is present but its NT value is absent | No NT value was recovered there; do not infer an empty password or nonexistent account. |
| Multiple sessions name the same account | Preserve each session and any differing values before considering deduplication. |
| Missing stream, template/signature error or truncated memory | Check acquisition completeness, dump architecture/Windows build and parser support. This is incomplete evidence, not proof that credentials were absent. |

Report the packages examined, identities actually associated, missing fields and errors without copying secret values into an ordinary summary. Ticket export via `--kerberos-dir` creates additional credential artifacts; it is unnecessary for the MSV task. Keep any separately authorised online validation outside this offline conclusion.

The [upstream project](https://github.com/skelsec/pypykatz) and [LSA CLI implementation](https://github.com/skelsec/pypykatz/blob/main/pypykatz/lsadecryptor/cmdhelper.py) help resolve reader and output differences.

## Derive an NT value from known text

`pypykatz crypto nt` computes the NT hash of its password argument locally. For an explicitly public fixture value:

~~~bash
pypykatz crypto nt 'Example-Only-Password!'
~~~

The calculation is MD4 of the exact password encoded as UTF-16LE, without a terminator; case and characters matter. It does not contact AD or confirm any account accepts the text. The output is a 16-byte value rendered as 32 hexadecimal characters. In RC4-HMAC Kerberos, this is the password-derived key; it is not an AES service key, a Kerberoast record or a captured NetNTLMv2 response.

The reviewed CLI accepts the password positionally, so quoting protects shell syntax but still exposes the expanded argument to process inspection and potentially history. Do not mistake it for a secret prompt or invent a stdin flag. Use this form for public fixtures or only where that exposure is explicitly acceptable; choose an established secret-input workflow otherwise. See the [crypto CLI](https://github.com/skelsec/pypykatz/blob/main/pypykatz/utils/crypto/cmdhelper.py), [NT implementation](https://github.com/skelsec/pypykatz/blob/main/pypykatz/utils/crypto/winhash.py) and [RC4-HMAC specification](https://www.rfc-editor.org/rfc/rfc4757.html).
