---
name: certipy
description: Enumerate AD CS templates and interpret Certipy findings from Linux. Use when selecting directory-only collection, identifying omitted CA evidence or separating template configuration from current certificate authentication behavior.
---

# Collect the evidence behind a template finding

Use ly4k's Certipy AD CS tool, commonly packaged as `certipy-ad`; an executable named `certipy` can belong to unrelated software. Confirm the banner and `find -h`. The walkthrough uses v4.8.2; use the installed generation's flags and output formats.

Define `certipy_bin` as the verified executable, `upn` as the known account UPN, `dc_ip` as the intended DC address, and `prefix` as a fresh absolute report prefix in a private directory. Start with directory-only collection:

~~~bash
umask 077
"$certipy_bin" find -u "$upn" -dc-ip "$dc_ip" -dc-only -text -json -output "$prefix"
~~~

Omitting the password prompts for it in the reviewed CLI. Supply the correct AD DNS/DC naming configuration; a public resolver or bare domain alias may not resolve service hostnames. Do not disable LDAP transport protections merely to make a connection succeed.

`-dc-only` omits CA security/configuration retrieval and Web Enrollment checks. Label those as uncollected. Full collection can contact CA RPC/Remote Registry endpoints and has historically caused RemoteRegistry to start; it is not equivalent to a directory-only query. Preserve collection errors alongside reports.

First retain the full directory result. `-vulnerable` filters findings according to the tool's rules and the selected account's nested groups; an empty filtered report is not a clean bill of health. For an ESC1 hypothesis, read the template's actual publication/enabled state, enrollment rights, subject/SAN control, authentication EKUs, approval/signature requirements and relevant CA policy together. A suggestive template name is insufficient. MachineAccountQuota is a separate directory setting and does not itself grant template enrollment rights.

Historical certificate issuance does not establish present authentication. Windows strong certificate-mapping enforcement changed after this 2023 writeup; inspect the issued certificate's SID/mapping information and the target's actual patch/configuration state. A SAN username alone does not guarantee that identity will authenticate. PKINIT and Schannel are different authentication paths; a PKINIT error alone neither invalidates every use of the certificate nor proves a universal workaround.

This skill stops at evidence collection and interpretation. Requests, account creation, template edits and delegation writes are separate operations with persistent state.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Authority pp. 9–13. Sources: [find CLI](https://github.com/ly4k/Certipy/blob/main/certipy/commands/parsers/find.py), [implementation](https://github.com/ly4k/Certipy/blob/main/certipy/commands/find.py), [Microsoft mapping enforcement](https://support.microsoft.com/en-us/servicing/os/windows-server/2022/05/kb5014754-certificate-based-authentication-changes-on-windows-domain-controllers).
