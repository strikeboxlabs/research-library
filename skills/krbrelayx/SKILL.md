---
name: krbrelayx
description: Relay a selected Kerberos authentication exchange to an AD CS web endpoint with krbrelayx from Linux. Use when NTLM is unavailable and callback DNS naming, SPN selection, listener routing and certificate identity need explicit evidence.
---


# Select the Kerberos relay and certificate outcome

Read this entire SKILL.md and [SMB-to-AD-CS relay](references/smb-to-adcs.md) before starting this task. Require the source machine, authorized enrollment target, DNS/SPN prerequisites and owned listener route. Finish with the actual relayed principal, issued certificate/private key and any separately requested authentication result; HTTP 200 or a PFX filename alone is insufficient.

Use dirkjanm's `krbrelayx.py`, with its compatible installed Impacket dependency. This package supports the relay task, not every unconstrained-delegation key/export mode in that toolkit. Define `script` as the reviewed local path and inspect `python3 "$script" -h`. Omitting account keys selects relay mode; supplying unconstrained-delegation keys changes the mode and evidence requirements.

For a known Web Enrollment target, an explicit template and subject, define `listen_ip` for the owned listener, `out` as an existing private output directory, `enrollment_url`, `template` and `victim` (including the trailing `$` for a computer). In a private working directory:

~~~bash
python3 "$script" -ip "$listen_ip" -l "$out" -t "$enrollment_url" --adcs --template "$template" -v "$victim"
~~~

Use the exact real enrollment URL and server identity. This startup can create SMB, HTTP and DNS listeners; inspect the installed implementation and their addresses/ports rather than assuming it exposes only SMB. A proxy wrapper can help supported outbound TCP connections but cannot supply inbound routing or carry DNS UDP automatically. Track every actual listener and its lifetime.

Keep the relay trace with certificate disposition, logged path and inspected certificate subject/SAN/SID. A generated CSR or request ID is not an issued credential. `unknown....pfx` can reflect incomplete identity inference; do not rename it to an assumed account and report authentication. Stop the owned listeners, reconcile the DNS record and perform the task's certificate/ticket lifecycle actions separately. See [upstream CLI](https://github.com/dirkjanm/krbrelayx/blob/master/krbrelayx.py).
