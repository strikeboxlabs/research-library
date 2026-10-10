# Eighth CTF writeup batch

Reviewed 2026-10-09. All three supplied Hack The Box writeups were processed: **57 physical PDF pages** were text-extracted and read, with **23 selected pages** rendered and visually inspected. This batch adds **eight independent tool skills** and enriches **six existing skills**, bringing the catalogue to **102**.

Each new package contains one `SKILL.md`. Workers need only selected skill folders; this report is maintenance evidence. Originals and intermediate material remain in ignored `ingest/` and `work/pdf-ingest-batch8/`.

## Coverage of all three documents

Page numbers are one-based physical PDF pages, including covers. Repeated commands were reviewed without adding duplicate instructions.

| Document | Pages | Accepted guidance |
|---|---:|---|
| `Bankrobber.pdf` | 17 | Prompt-synchronized pwntools exchanges, byte strings, positive completion evidence and timeout/EOF handling (14); matching Metasploit pattern generation/lookup, exact versus heuristic offsets and identifying the affected field (15–16). Existing MySQL, Chisel, SMB and packet-capture guidance already covers the portable decisions elsewhere in the writeup. |
| `Bastion.pdf` | 10 | Linux 7-Zip inspection of supported disk-image layers, adapted from the GUI workflow (4–5); matching SYSTEM/SAM input and legacy extraction limitations (5); OpenSSH transfer protocol, Windows-path quoting and file completeness (8). |
| `BigBang.pdf` | 30 | WPScan enumeration and confidence (3); PHP CLI/web configuration, PHAR version behavior and image-header limitations (4–8); incomplete ELF evidence (8); phpass and process budgeting (11–12); coherent database transfer, Grafana conversion and PBKDF2 representation (13–14); selected-device ADB, routing, privilege context and trust-store limits (15–23); OpenSSL subject-hash naming (19–20). Screenshot-only application actions and final request/callback evidence were also reviewed (24–30). |

New skills: `adb`, `grafana2hashcat`, `msf-pattern`, `php`, `pwntools`, `samdump2`, `scp`, `wpscan`.

Enriched skills: `7z`, `file`, `hashcat`, `john`, `openssl`, `readelf`.

## Corrections and useful distinctions

- **Protocol results and offsets:** Bankrobber's `range(0, 9999)` omits 9999 despite the prose claiming every four-digit PIN. Its Python 2-style string exchange also needs byte-aware handling in Python 3. Absence of an access-denied phrase can instead mean timeout, truncated reply or another protocol response. The accepted skill uses explicit synchronization and positive completion, without turning the walkthrough's guessing loop into a default workflow. Metasploit's generator adds a newline, the lookup's default length is 8192, and a possible match is not an exact match. Its observed overwrite affects a binary-path field, not a demonstrated saved return address. The value 32 is case-specific.
- **Web and database inference:** an image resource callback alone does not prove JavaScript execution or administrator identity; the later event-handler behavior is separate evidence. A user identifier of 3 does not prove that users 1 and 2 exist. SQL `ORDER BY` results concern the selected result's width, not every table's schema. SQL identity named root does not establish OS root or every database privilege. The PHP check for `::1` is specifically IPv6 loopback. Existing MySQL/transport skills already contain the relevant privilege and endpoint distinctions.
- **Disk images and hives:** a large VHD does not require switching to Windows, and the outer container may expose another image layer. Linux support must be checked in the installed 7-Zip build. `samdump2 SYSTEM SAM` extracts records; it does not crack them. The reviewed 3.0.0 source uses legacy cryptographic handling and substitutes the empty-password NT hash when the NT field does not have its expected legacy size. Plausible output therefore does not prove modern hive support or an empty password. Its disabled-account annotation describes acquisition-time state. Private hashes should not be uploaded to the writeup's online cracking service.
- **Transfer semantics:** Bastion's unquoted backslashes are unsafe to copy into a Linux shell. Current OpenSSH scp defaults to SFTP; a Windows command-prompt path and an SFTP path are not interchangeable assumptions. Legacy `-O` changes remote-shell interpretation. BigBang's live `grafana.db` copy is not evidence of a coherent SQLite backup, especially with journal/WAL state. SQLite's writer-version metadata does not identify the Grafana release or its password parameters.
- **WordPress detection:** WPScan's candidate inventory and detection mode are separate controls. A readme stable-tag version and its confidence are evidence to verify, not proof of deployed vulnerable code. Passive detection still sends requests; a missing API annotation does not mean no known vulnerabilities. Core, plugin and plugin-version detection settings can differ, and a bare enumeration flag can expand scope beyond plugins.
- **PHP and recovered bytes:** the local PHP executable, its SAPI/configuration and the observed server header are distinct. PHP 8.0 changed automatic PHAR metadata deserialization. `getimagesize` can accept non-images and produce meaningless dimensions, so the GIF prefix does not establish a valid image. Appending 16 NUL bytes to a truncated libc may make a parser proceed but does not recover the missing bytes or prove that they are irrelevant. A fixed response-prefix length also needs evidence from the actual transformation; it is not a universal repair.
- **Offline formats:** preserve complete phpass records and establish the algorithm from the record/application, rather than assuming every WordPress release uses it. John's `--fork` creates processes and can combine with OpenMP threads. The reviewed iamaldi Grafana converter hardcodes 10,000 PBKDF2-SHA256 iterations, encodes the literal salt as UTF-8 and hex-decodes the digest before base64. Its stdout contains banners; `-o` produces the intended records. Its printed Hashcat `--wordlist` is not the documented dictionary-input option; the accepted examples supply the dictionary positionally. Conversion is not password recovery or validation of the chosen cost.
- **Android and certificate context:** the emulator's loopback is not the workstation's loopback, and a workstation loopback-only SSH listener does not become reachable on every interface. ADB reverse mappings are one explicit device-to-host route. Device-wide proxy settings need prior-state restoration and may be ignored by an app. Root obtained inside one shell does not elevate later ADB transfers. A historical remount-and-copy recipe does not establish a writable or identical CA store on another build. OpenSSL's old subject hash is a directory lookup key with possible numbered collisions, not a fingerprint. CA presence, app trust, cleartext policy and certificate pinning are different conditions. The shown Bash hosts-file examples also contain backticks that invoke command substitution; they were not copied.

Primary manuals/source are linked inside every accepted package. Their current semantics take precedence over historical walkthrough defaults.

## Reviewed material not turned into skills

| Material | Decision and remaining work |
|---|---|
| Bankrobber's cookie theft, SQL injection and executable-path overwrite chain | Retained the reusable protocol, offset and interpretation lessons. Application-specific payloads, PIN enumeration, credential replay and callback binaries are not necessary for these utility skills. No target interaction was performed. |
| Bastion's mRemoteNG GUI credential display | The source demonstrates a GUI configuration-recovery workflow, not a Linux CLI utility. A Linux alternative needs separate review of configuration versions, encryption parameters and actual parser support. No universal claim that a displayed version's storage is fixed or broken was imported. |
| BigBang's wrapwrap and custom iconv exploit adaptation | Reviewed the supplied usage and the [upstream wrapwrap overview](https://github.com/ambionics/wrapwrap). This filter-chain generator and the application-specific exploit require a controlled byte-exact fixture before accepting claims about prefixes, output length or binary recovery. PHP and ELF skills retain the supported interpretation lessons; no exploit repair or payload pipeline was packaged. |
| BigBang's Genymotion/Burp GUI and application command-injection chain | ADB contributes a Linux CLI workflow; emulator installation, account-specific GUI actions and application payloads remain context. Rejected punctuation does not prove a complete input filter, and a correlated ICMP callback alone does not establish execution identity or full command semantics. |
| Repeated Nmap, MySQL, Chisel, SMB, SSH, curl, SQLite, packet capture and shell commands | Existing coverage was retained where it already resolved the demonstrated decision. No filler skills or duplicate runtime references were added. |

All three PDFs are processed. Deferred material is a coverage decision, not unread input. The working tree was clean at the start; previous batches and unrelated assessment methodology were preserved.

## Source fingerprints and local checks

SHA-256 identifies the exact originals even after the ignored inbox is replaced.

| File | SHA-256 |
|---|---|
| Bankrobber.pdf | `6011892235619fa04836ce74a46cabea6d0da6d2a7447e378e52492a8a005164` |
| Bastion.pdf | `23133da636f143557d6dfb317fe895aced46ab45206e61b0c2594eae3b44d945` |
| BigBang.pdf | `232d46993cdf241ac583c85931c1e3a0142b4344f4bae58df28f1f4a70268370` |

The reviewed Grafana converter was exercised locally on Windows with two synthetic records, including a non-ASCII salt, against independently constructed PBKDF2/base64 expectations. Both matched; the `-o` file excluded banners, and a header-bearing input was rejected without creating an output file. No password recovery was attempted. Reviewed converter SHA-256: `bcebba5c2cf8fad98c696e834c368dc9924940c9063c663a419b9318eeed91c0`. The pwntools example was checked for Python syntax, without importing pwntools or opening a connection.

Outdated WPScan source paths and an unavailable samdump2 mirror returned 404; the current WPScan repository tree and Debian's packaged upstream source resolved those lookups. Extraction and selected-page rendering completed without warnings.

See the [validation record](validation.md) for repository checks and the [Linux adaptation guide](../GETTING_STARTED.md#2-adapt-to-this-machine) for installed-help and fixture validation on the intended host.

## Source notes retained for the 2026-10-10 pilot

The original review/source footers for the three revised batch-8 skills are retained here. Their worker instructions now contain operational conditions, worked results and selected documentation links. Historical execution coverage remains as stated below; these notes do not require worker reads.

**pwntools:** Documentation reviewed 2026-10-09; Linux execution untested. Case: Bankrobber pp. 14–16. Sources: [tube behavior](https://docs.pwntools.com/en/stable/tubes.html), [cyclic patterns](https://docs.pwntools.com/en/stable/util/cyclic.html).

**scp:** Documentation reviewed 2026-10-09; Linux execution untested. Cases: Bastion p. 8; BigBang p. 13. Source: [OpenSSH scp manual](https://man.openbsd.org/scp).

**grafana2hashcat:** Documentation reviewed 2026-10-09; two synthetic conversion records and header rejection checked on Windows. Linux execution untested. Case: BigBang pp. 13–14. Sources: [converter implementation](https://github.com/iamaldi/grafana2hashcat/blob/main/grafana2hashcat.py), [historical Grafana parameters](https://github.com/iamaldi/grafana2hashcat/blob/main/README.md), [Hashcat mode parser](https://github.com/hashcat/hashcat/blob/master/src/modules/module_10900.c), [Hashcat syntax](https://hashcat.net/wiki/doku.php?id=hashcat).

## Coverage correction — 2026-10-10

The historical deferrals above are not current acceptance rules. The [coverage repair record](ctf-writeups-overnight-2026-10-10.md#coverage-repair-after-the-crossfit-review--2026-10-10) maps newly accepted independent tools and deeper procedures back to these sources. Overlap, short invocations and an unavailable Linux fixture no longer disqualify documentation-supported tasks; authoring execution restrictions do not prohibit documenting authorized operations. Original page coverage and test history remain unchanged.
