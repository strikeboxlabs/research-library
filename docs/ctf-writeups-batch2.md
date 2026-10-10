# Second CTF writeup batch

Reviewed 2026-10-09. Five additional user-supplied Hack The Box writeups contain 94 physical PDF pages. All pages were text-extracted and read; 29 relevant pages were rendered and visually inspected, including screenshots with command details. The batch adds 13 independent skills and enriches five existing ones, bringing the catalogue to 30.

Each new tool is one `skills/<tool>/SKILL.md`, with concise source links and no dependency on another skill, these notes or the PDFs. Instructions assume a worker already competent with the CLI. The additions capture reusable decisions, execution details and failure interpretation rather than retelling each compromise chain.

## Source coverage

Page numbers below are one-based physical PDF pages, including covers.

| Document | Pages | Accepted guidance |
|---|---:|---|
| `Administrator.pdf` | 11 | BloodHound.py generation, collection and NTLM fallback (3–4); Evil-WinRM (5, 8, 11); binary FTP/Password Safe v3 (7); NetExec credential pairing (8); SPN-write distinction (9–10); selected-account replication audit (10). |
| `Admirer.pdf` | 23 | Parent-path 403 versus readable children (4–5); FTP (7–8); MySQL client/server file boundary (11–16); sudo environment/export semantics (21–22). |
| `AdmirerToo.pdf` | 24 | Wfuzz Host-header comparison (3–4); Gobuster paths (5–6); tcpdump evidence (11–12); ss listeners and process visibility (15–16); SSH forwarding (17); strace config lookup (19). |
| `Aero.pdf` | 14 | Default Nmap port coverage and `-A` interpretation (2). The remaining exploit development is predominantly Windows-specific. |
| `Agile.pdf` | 22 | Nmap coverage (2); Gobuster redirects/authentication context (3); MySQL inspection (13–14); Bash redirection order and live listener checks (17); SSH forwarding (18); sudoedit and startup/source behaviour (20–22). |

The source files remain unchanged in the ignored `ingest/` inbox as of this review. Extracted text, images and primary-source snapshots are in ignored `work/pdf-ingest-batch2/`. They are authoring material, not installed worker resources. The inbox may be replaced with later batches; the page mapping and fingerprints below identify this batch independently.

## New and enriched skills

New: `bash`, `bloodhound-python`, `evil-winrm`, `ftp`, `gobuster`, `mysql`, `netexec`, `ss`, `ssh`, `strace`, `sudo`, `tcpdump`, `wfuzz`.

Enriched: `dirsearch`, `hashcat`, `impacket-getuserspns`, `impacket-secretsdump`, `nmap`. Secretsdump now distinguishes its original local hive procedure from a selected-account remote replication audit. Its description and catalogue entry reflect that expanded scope.

Important corrections retained:

- **Nmap:** the Aero/Agile default scans do not cover all TCP ports. `-A` changes interrogation features, not port coverage. Report observed results within the scanned range.
- **BloodHound:** Administrator's log identifies a legacy collector and NTLM fallback despite the Kerberos option. CE/legacy compatibility, actual authentication and completed collection/import are separate checks. Directory-only collection avoids unnecessary member-host probes.
- **NetExec:** two independent credential files can create every username/password combination. Paired mode, single-password behaviour and stopping after a success affect the meaning and scope of the result.
- **FTP/Hashcat:** Administrator transfers a binary database in ASCII mode. The reusable guidance explicitly selects binary transfer. Current Hashcat mode 5200 consumes the Password Safe v3 file and disables potfiles; it needs an explicit results file, unlike the existing NT/Kerberos examples.
- **AD operations:** requesting a ticket for an existing SPN is different from temporarily writing an SPN. Replication requests require applicable directory rights; an authorized user need not be a DC machine account. The new secretsdump example selects one subject and NTLM material rather than copying an unrestricted directory extraction.
- **Shell/sudo:** Admirer's shell assignment does not establish an exported variable, so its failed `sudo -E` example does not prove a universal preservation rule. Agile's `2>&1 >/dev/null` discards stdout only. Its user-versus-system bashrc explanation is not a general startup rule. Sourcing executes code as the caller; a file's owner does not supply the execution identity.
- **Sudo patches:** an upstream version string alone cannot decide whether a distribution build has the sudoedit fix. [Ubuntu's advisory](https://ubuntu.com/security/CVE-2023-22809) explicitly lists fixed builds retaining older upstream versions.
- **Runtime evidence:** a configuration file or debug flag is not proof of a live listener. The Agile browser-debug endpoint is explicitly enabled in Chrome's launch arguments, not a universal Selenium default. Strace's failed config lookup proves an attempt, not that the file was read. Packet arrival proves the observed packet, not an entire application exploit chain.

Primary manuals/source are linked in the individual skills. They were checked against the walkthrough claims, including rolling upstream implementation details; they are not guarantees about versions installed on the eventual Linux server.

## Deferred work

| Candidate | Why it needs more than this writeup |
|---|---|
| targetedKerberoast, AD password resets and other directory writes | A dedicated skill needs exact prior-state capture, write prerequisites and tested restoration after partial failure. The current GetUserSPNs skill explains the boundary. |
| phpggc and application-specific deserialization chains | Need compatible gadget/version selection and a disposable reproduction with evidence of each prerequisite, not just a copied payload. |
| WHOIS, fail2ban, systemctl | The writeup demonstrates one configuration-dependent chain. Strace/ss cover the portable diagnostic lessons; separate utility skills need a broader task/error workflow. |
| Netcat/Ncat and terminal handling | EOF behaviour, listener flags and PTY recovery vary by implementation. Avoid presenting the writeups' interchangeable `nc`/`ncat`/Windows `nc64` usage as portable. |
| Rustbuster, linPEAS, tar, curl and Python utilities | Either overlap the accepted path-discovery/file-inspection tasks or lack enough additional tool-specific decisions here to justify another skill yet. |
| ThemeBleed/CLFS and other Windows-native payload steps | Outside this Linux CLI catalogue; Aero primarily informs scan interpretation. |
| Werkzeug debugger and Chrome DevTools GUI chains | Application/GUI workflows need their own version-specific evidence. SSH forwarding is the accepted reusable CLI component. |

## Source fingerprints

SHA-256 of the exact supplied PDFs:

| File | SHA-256 |
|---|---|
| Administrator.pdf | `f8b7683090e64e6110206e84417318a06c6adaa4a2e911373743058333227816` |
| Admirer.pdf | `8e16ef855d1f5318fcb96fbd7c811fe103b75a938575163ed30d4708ca48242e` |
| AdmirerToo.pdf | `abc505e9ed48884bcdbefd32f56cdf0bda1e50669d7cfb18779704188ff6431b` |
| Aero.pdf | `e31182234884c8700d138e94f241b2661dbe98451c298d1c05eb8e2061fbb68e` |
| Agile.pdf | `aca9b57bf43851e41bc4fde893b6bf7c50a63a885f22b702ad113459027ef86a` |

See the [validation record](validation.md) for checks actually run. Linux procedure execution and agent usefulness remain untested. Use the existing [host-adaptation workflow](../GETTING_STARTED.md#2-adapt-to-this-machine) to adapt selected skills to the real Linux machine and exercise success and failure cases. No writeup targets were contacted or supplied credentials/flags copied into skills.

## Coverage correction — 2026-10-10

The historical deferrals above are not current acceptance rules. The [coverage repair record](ctf-writeups-overnight-2026-10-10.md#coverage-repair-after-the-crossfit-review--2026-10-10) maps newly accepted independent tools and deeper procedures back to these sources. Overlap, short invocations and an unavailable Linux fixture no longer disqualify documentation-supported tasks; authoring execution restrictions do not prohibit documenting authorized operations. Original page coverage and test history remain unchanged.
