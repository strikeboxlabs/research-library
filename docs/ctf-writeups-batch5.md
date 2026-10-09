# Fifth CTF writeup batch

Reviewed 2026-10-09. All four supplied Hack The Box writeups were processed: **83 physical PDF pages** were text-extracted and read, with **32 selected pages** rendered and visually inspected. This batch adds **13 independent tool skills** and enriches **seven existing skills**, bringing the catalogue to **78**.

Each new package contains one `SKILL.md`. Existing GDB and OpenSSL packages gain conditional references for live debugging and PKCS#12 handling respectively. GDB's existing core-dump command and diagnostic workflow remain intact. Workers need only selected skill folders; there is no umbrella, mandatory provenance file or sibling dependency. Originals and intermediate evidence remain in ignored `ingest/` and `work/pdf-ingest-batch5/`.

## Coverage of all four documents

Page numbers are one-based physical PDF pages, including covers. Repeated commands were reviewed without padding existing skills.

| Document | Pages | Accepted guidance |
|---|---:|---|
| `Attended.pdf` | 35 | SMTP recipient interpretation (4); S-nail identity and message construction (5–8); controlled Vim startup and swap recovery (8–9, 15); OpenBSD FTP URL fetching (10); executable SSH configuration (16); public/private key identity and encoding (18–21, 26–31); live GDB, disassembly, ELF address spaces and complete gadget effects (20–25); byte inspection/reconstruction (30–31). |
| `Authority.pdf` | 14 | Inline Ansible Vault extraction, mode 16900 and decryption (5–8); Certipy directory-only inventory and template evidence (9–12); PKCS#12 separation, authentication-path distinctions and existing-delegation service tickets (12–14). |
| `Awkward.pdf` | 26 | Application-derived SHA-256 and HS256 JWT checks (8–9, 14–15); fixed awk programs, quoted CSV and binary-transfer interpretation (13–18); partial/nested archive recovery (17–18); GNU Mailutils option injection and implementation differences (24). |
| `Axlle.pdf` | 8 | Swaks MIME attachments, valid headers, explicit SMTP destination and submission evidence (4). Collector, Windows payload and scheduled-job material was also reviewed; scope decisions appear below. |

New skills: `ansible-vault`, `awk`, `certipy`, `impacket-getst`, `mail`, `objdump`, `readelf`, `ropgadget`, `smtp-user-enum`, `ssh-keygen`, `swaks`, `vim`, `xxd`.

Enriched skills: `ftp`, `gdb`, `hashcat`, `john`, `openssl`, `ssh`, `tar`.

## Corrections and useful distinctions

- **SMTP and mail implementations:** smtp-user-enum's broad positive classification does not verify mailbox existence. Candidate/control comparison and the actual SMTP stage matter; even a positive recipient response can be deferred validation. S-nail and GNU Mailutils assign different meanings to `-a`. An unquoted subject can introduce Mailutils options, including command execution. Swaks needs a complete `Subject: value` header; MIME inspection, recipient acceptance, submission and attachment execution are separate observations.
- **Vault objects:** inline Ansible values are encrypted data, not ordinary password hashes. Extract each full vault object before conversion, retain its variable mapping, and distinguish the recovered vault password from the decrypted value. The intended CLI comes from Ansible/ansible-core, not an inferred similarly named package. Explicit output avoids decrypting the input in place.
- **AD CS and Kerberos:** the source's Certipy v4.8.2 behavior is not a universal current interface. Directory-only collection omits CA/RPC/web evidence; full collection can have service effects. Template publication, rights and policy must be considered together. Microsoft's certificate-mapping enforcement changed after the writeup, so its SAN-based result is not a promise for current patched DCs. PKINIT and Schannel failures require different interpretation. The normal getST result is a service ticket, not a TGT for arbitrary services. PassTheCert's delegation write changes directory state; it is not merely a login check.
- **PKCS#12:** bundle import passwords and encrypted output-key passphrases are different. The accepted extraction retains private-key encryption. A diagnosed legacy-algorithm/provider failure is different from a bad password; neither justifies disabling integrity checking or globally weakening TLS.
- **Debugger and binary evidence:** Attended targets OpenBSD. Linux-hosted static inspection does not imply Linux execution compatibility or matching syscall conventions. `objdump -s` is a byte dump; `-S` is source-interleaved disassembly. Static section bytes are distinct from memory after input processing. Runtime addresses need the actual mapping/build. GDB's ASLR setting can change a reproduction. Complete gadget sequences matter: `not al` can have adjacent clobbers, `shr eax` is not an AL-only operation, and scalar float-to-integer conversion is not a bitwise copy.
- **Keys and byte formats:** sshd's `%k` token passes offered public key/certificate data, not a private key. OpenSSH private-key envelopes and public-key blobs have different layouts; the source's fixed offsets and oversized key are specific to its fixture. Xxd reverse mode can patch without truncation and can skip malformed input. Inspect a fresh reconstructed artifact rather than trusting status or a correct prefix.
- **Configuration and partial artifacts:** `ssh -G` can still evaluate `Match exec`; config inspection is not automatically free of execution. Vim startup/modeline controls must apply before loading the artifact, and read-only mode is not a sandbox. Swap recovery can depend on the original file. An awk-backed transfer is not guaranteed byte-preserving, but the writeup alone does not identify the precise corruption cause. Useful members from a failed outer archive need separate checks; a valid inner archive does not establish completeness of the outer one.
- **Password records:** a 64-character hexadecimal string does not establish SHA-256. Jumbo's HS256 JWT path needs the original compact token and the right supported parser. Re-serializing decoded JSON changes the signed bytes. No source credentials, private tokens or recovered values were copied into portable examples.

Primary manuals and implementations are linked inside each accepted package. The changes are documentation-reviewed; current-source semantics do not establish historical package compatibility or Linux execution success.

## Reviewed material not turned into skills

| Material | Decision and remaining work |
|---|---|
| Attended's modeline payload, custom HTTP command channel and final key-overflow/ROP script | Retained editor startup, debugger and binary-format lessons. A complete exploit/C2 framework is not a general utility skill. Its final invocation includes an `--offset` argument not defined by the displayed parser, so the printed script is not replayable verbatim. Historical runtime dependencies and target-specific addresses need a separate controlled fixture. |
| Authority's machine-account creation, PassTheCert delegation write and broad replication dump | These are persistent directory changes or broader collection than needed for the accepted guidance. A separate procedure would need exact target/state ownership and restoration evidence. Existing selected-account secretsdump guidance already covers the reusable collection distinction. The getST skill tests established delegation; it does not create it. |
| Awkward's application-specific SSRF scan, JWT rewriting and symlink/job chain | Retained input interpretation and tool-level failure lessons. The broad port loop and application behavior need an explicit application fixture before becoming a reusable methodology. Existing pspy guidance already covers incomplete process evidence; timestamps alone do not prove the causal privileged operation. |
| Axlle's Nim/XLL payload, Metasploit handler, directory password reset and Windows StandaloneRunner chain | Reviewed as context, not promoted into generic Linux CLI instructions. A handler excerpt is insufficient for a coherent Metasploit skill. Account password changes need explicit ownership and recovery planning. The final shown identity is Administrator; a SYSTEM claim cannot be inferred merely from the described scheduled-job configuration. |
| Repeated Nmap, Gobuster, LDAP, BloodHound, SMB, curl and ordinary copy commands | Existing skills cover the demonstrated decisions. No additional prose was added solely to repeat tool appearances. GUI and native Windows commands remain source context. |

All four PDFs are processed; these are deliberate coverage decisions, not unread documents. Unrelated assessment methodologies and pre-existing uncommitted work were preserved.

## Source fingerprints

SHA-256 identifies the exact originals even after the ignored inbox is replaced.

| File | SHA-256 |
|---|---|
| Attended.pdf | `604fa5f70b09863b4f8cddbefbd2be8894255a8d6bdba7b2ab19eef9743a7136` |
| Authority.pdf | `34f8b49d223cf3beb2e408d2d88828e2cbe7e48099c01b55d0d0e919bfd6dc22` |
| Awkward.pdf | `b74dc55bf8a880f7a3981ae5676378d9fa3b95ce58ea319e8d042b62bd0d2f54` |
| Axlle.pdf | `cbf548ee1a8f609ae62082ad0c8e992ad463314bc237b4ff1564cd3b266ce4c8` |

See the [validation record](validation.md) for checks actually executed. The [Linux adaptation guide](../GETTING_STARTED.md#2-adapt-to-this-machine) describes installed-help checks and meaningful success/failure fixtures on the intended host.
