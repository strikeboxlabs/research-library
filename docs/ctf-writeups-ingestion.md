# First CTF writeup batch

Reviewed 2026-10-09. Five user-supplied Hack The Box writeups, 80 PDF pages in total, informed 16 new independent CLI skills. Each addition is one `SKILL.md` with concise upstream source links. Workers need neither the PDFs nor this ingestion record. The existing GDB skill and assessment methodology were preserved.

All pages were text-extracted and read. Thirty-three relevant pages were rendered and visually inspected, including command screenshots omitted from text extraction. Walkthrough commands were treated as evidence and checked against upstream manuals/source or the relevant distribution's own documentation. No writeup targets were contacted and no credentials, tickets or flags were copied into skills.

Page references below are one-based physical PDF pages. Cover dates are historical context, not a guarantee that every screenshot reflects that date.

| Supplied document | Pages | Guidance accepted in this batch |
|---|---:|---|
| `Absolute.pdf` | 21 | Nmap (2–3); ExifTool (4–5); GetNPUsers/John (5–6); getTGT/ldapsearch (7–9). |
| `Academy.pdf` | 16 | Nmap (3); dirsearch (4–5); aureport/TTY evidence (13–14). |
| `Access.pdf` | 14 | Nmap scan handoff pitfalls (3); MDB Tools (5); 7-Zip (6); readpst (7). |
| `Active.pdf` | 10 | Nmap (2); Samba smbclient (3–6); gpp-decrypt (4–5); ldapsearch/GetUserSPNs (6–9); Hashcat (9). |
| `Acute.pdf` | 19 | Nmap (2); ExifTool (4–5); offline secretsdump and John (15–16). |

Original PDFs were read without modification from the local `ingest/` inbox, which is ignored by Git and can rotate between batches. Extracted text, page images and research snapshots are in ignored `work/pdf-ingest/`. The catalogue and each skill retain the durable source trail. This repository does not need to redistribute the writeups to deliver the skills.

## Corrections carried into the skills

- **Scan handoffs:** the repeated human-output pipelines discard useful state, and Access's pipeline loses the distinction between TCP and UDP. Keep protocol-specific evidence and use XML for automation. Full TCP discovery does not establish UDP coverage.
- **Metadata:** Absolute's screenshot contains both Artist and Author fields. Searching only one printed label and splitting names at spaces can omit or damage candidate identities. Metadata is a lead, not account verification.
- **LDAP:** Absolute describes `ldapsearch -x` as NTLM; it actually selects simple bind. Its bare `user` filter and fixed `CN=Users` base were replaced with explicit LDAP filters and base discovery. Error `52f` alone does not establish Protected Users membership. StartTLS, Kerberos prerequisites and incomplete results are distinguished.
- **Kerberos:** AS-REP password-testing material, a usable credential cache and service-ticket material are different artifacts. Encryption type matters. GetUserSPNs' output-file switch can enable ticket requests, so it is excluded from the enumeration-only example.
- **TTY logs:** Academy's password-capture description is too broad. The Linux-PAM documentation describes default exclusions and `log_passwd`; the skill also accounts for session context and user-ID interpretation on another machine.
- **Archive/mail inspection:** unsupported ZIP encryption does not prove corruption or a bad password. Readpst's type and output switches have different meanings; individual email files are sufficient for the supported task.
- **Password tools:** the skills preserve results and select formats explicitly; Active's `--force --potfile-disable` is not copied as a default. Two unrelated `gpp-decrypt` implementations require different syntax.

These are source-review conclusions. Links to the applicable primary material are in each skill; rolling upstream branches were reviewed on the date above and are not installed-version guarantees.

## Remaining candidates

This is a first batch, not a skill for every executable mentioned. The next additions should close a demonstrated guidance gap:

The [second batch](ctf-writeups-batch2.md) subsequently added BloodHound.py, FTP and Evil-WinRM guidance; Linux execution remains pending. The table below preserves the original candidate assessment, including candidates not yet covered.

| Candidate and source | What another skill needs |
|---|---|
| BloodHound.py, Absolute 12–14 | Check the chosen collector and server generation, Kerberos options, collection scope and import compatibility. The historical fork/Neo4j recipe should not be adopted automatically. |
| Certipy, bloodyAD, owneredit, dacledit, Absolute 14–16 | Separate discovery from object modification; verify current prerequisites, precise changes, restoration behaviour and partial-failure handling in an AD fixture. |
| Impacket smbclient, Absolute 9–10; smbmap, Active 3–6 | Distinguish their own syntax/authentication from Samba and verify whether permission probes write temporary objects. |
| masscan, Access 3 and Active 2 | Preserve protocol and target identity in the handoff, validate interface selection and rate/loss behaviour. |
| FTP client, Access 4 | Select the actual implementation; test binary transfers and passive/active data-channel failures. The broad firewall change is not reusable guidance. |
| username-anarchy, Absolute 5 | Preserve complete input names and evaluate candidate formats without implying that generated names exist. |
| Composer, Academy 15 | Define a useful script/plugin execution task and privilege boundary; verify behaviour beyond the walkthrough's single elevated-shell recipe. |
| Evil-WinRM, Absolute 16; wmiexec, Active 10 | Cover remote session prerequisites, output handling and cleanup with a suitable fixture. |
| msfvenom/msfconsole, Acute 8–11; netcat/terminal handling, Academy 11 | Design bounded guidance for payload/handler agreement or terminal recovery instead of copying an entire exploit chain. |

Windows-native steps such as `cmdkey`, `runas`, JEA/PowerShell commands, KrbRelay and Mimikatz are outside the Linux CLI catalogue. GUI Burp/Wireshark steps do not by themselves establish CLI procedures. Routine `cat`, `grep`, `wget`, `git` and similar usage supplied no sufficient new guidance for separate skills here.

## Linux follow-through

Use the [host-adaptation workflow](../GETTING_STARTED.md#2-adapt-to-this-machine) for the selected tools. Start with disposable local artifacts for metadata, archives, mail, audit logs and password-format handling. Exercise directory/network skills against an explicitly scoped lab, including denied/empty/expired or incomplete cases. Keep installed versions and evidence in `work/` or `runs/`, and record only portable corrections and actual results. [Validation](validation.md) distinguishes packaging checks from tool execution and agent outcomes.

## Coverage correction — 2026-10-10

The historical deferrals above are not current acceptance rules. The [coverage repair record](ctf-writeups-overnight-2026-10-10.md#coverage-repair-after-the-crossfit-review--2026-10-10) maps newly accepted independent tools and deeper procedures back to these sources. Overlap, short invocations and an unavailable Linux fixture no longer disqualify documentation-supported tasks; authoring execution restrictions do not prohibit documenting authorized operations. Original page coverage and test history remain unchanged.
