# Fourth CTF writeup batch

Reviewed 2026-10-09. All five supplied Hack The Box writeups were processed: **93 physical PDF pages** were text-extracted and read, with **27 selected pages** rendered and visually inspected. The batch adds **14 independent tool skills** and enriches **four existing skills**, bringing the catalogue to **65**.

Each new skill is one `SKILL.md`. Hashcat gains one conditional reference for binary containers, moving its existing Password Safe procedure alongside the new LUKS1 procedure. Workers only need that reference for those formats. There is no umbrella skill, required provenance file or dependency on another skill's folder. Originals, extracted text, rendered pages and primary-source snapshots remain in ignored `ingest/` and `work/pdf-ingest-batch4/`.

## Coverage of all five documents

Page numbers are one-based physical PDF pages, including covers. Repeated commands were reviewed without duplicating guidance that the existing skills already cover.

| Document | Pages | Guidance accepted from this source |
|---|---:|---|
| `Arkham.pdf` | 22 | CIFS mounting (4); LUKS layout, byte extraction and Hashcat binary input (5); Java serialization generation and runtime conditions (7–12); wrapped base64 transfer (13–14); OST conversion and image attachments (14–15). |
| `Armageddon.pdf` | 13 | MySQL batch queries (6–7); Drupal password-record mode (7–8); snap installation modes/hooks and sudo argument interpretation (10–12). |
| `Artificial.pdf` | 15 | Docker/Python wheel reproduction and local execution during model construction (4–5); SQLite inspection and application hash interpretation (6); tar backup and SQLite sidecars (8); wrapped bcrypt record (11); restic repository access, selected restoration and executable credential helper (9–14). |
| `Atlas.pdf` | 27 | Castor/marshalsec selection (9–11); ysoserial, producer-runtime isolation and RMI-stage evidence (11–14). GUI analysis and application-specific decryption in the remaining pages were reviewed as context, as detailed below. |
| `Atom.pdf` | 16 | Redis endpoint/value interpretation (3, 13–15); SMBMap share traversal/downloads (6–7); binary-digest base64 representation (11). |

New skills: `base64`, `cryptsetup`, `dd`, `docker`, `marshalsec`, `mount-cifs`, `pip`, `redis-cli`, `restic`, `smbmap`, `snap`, `sqlite3`, `tar`, `ysoserial`.

Enriched skills: `hashcat`, `mysql`, `readpst`, `sudo`. Earlier deferrals for base64, sqlite3 and basic archive handling are now addressed because these sources expose concrete corruption, consistency and extraction pitfalls. This is selective task coverage, not a full manual for every tool.

## Corrections and useful distinctions

- **LUKS and exact extents:** Arkham's 4097 sectors only fit its demonstrated layout. The current Hashcat LUKS1 parser reads keyslot material plus 512 encrypted payload bytes at the actual payload offset. It rejects LUKS2 and disables potfiles. The skill uses an intact image copy and explicit recovery output; a header backup is not automatically valid input. Candidate recovery needs verification with cryptsetup. GNU dd can stop successfully at early EOF, so copy status alone is insufficient.
- **Mounting:** a large SMB file does not require a kernel mount. CIFS inspection uses a dedicated read-only mount and verifies it actually succeeded. Unlocking LUKS is separate from mounting the inner filesystem. Plain filesystem `ro` can still replay an ext3/ext4 journal; the documented ext4 path uses a read-only mapping and `noload` with its consistency limitation.
- **Encoding and mail:** Arkham dismisses a base64 decode error; the accepted workflow treats its output as potentially partial. Strip the observed text envelope explicitly, not arbitrary characters. Atom's checksum field encodes raw SHA-512 bytes, not the displayed hexadecimal string. Readpst has format-specific OST support; relevant attachment images still need visual reading and checked transcription.
- **Hashes and queries:** Drupal `$S$` records use mode 7900; base64-wrapped bcrypt must first become the complete bcrypt record for mode 3200. A 32-character hex string alone does not establish MD5. MySQL batch mode changes interaction/output, not SQL side effects; the examples select actual bounded columns rather than copying full credential-table dumps.
- **SQLite and backups:** a wrong SQLite filename can create a misleading empty database. Explicit read-only opening prevents that mistake, while WAL consistency remains a separate acquisition issue. Artificial's backup includes database sidecars, so taking only the primary file may omit committed data. Extraction does not establish that the application backup itself was consistent.
- **Runtime reproduction:** Artificial's wheel has specific interpreter/ABI/platform constraints. Building/loading a model can execute code on the producer, as its local connection failure demonstrates. Docker bind sources belong to the daemon host; a writable whole-directory root mount is unnecessary for this fixture pattern. Preserve outputs outside the disposable container layer.
- **Java tooling:** select the actual unmarshalling format and gadget dependencies. Marshalsec `-t` unmarshals locally and `-a` expands the selected test. A generator's JDK failure is distinct from target rejection. Preserve ysoserial's binary stdout without text stripping. RMI/JNDI contact, resource retrieval and execution are separate observations; a generic TCP listener is not a replacement for the protocol server.
- **State-changing inspection surprises:** SMBMap normally attempts write-permission probes, so inventory examples disable them. Current `-r`/`--depth` syntax replaces assumptions from old `-R` examples. Snap `--dangerous` changes assertion checks, while devmode/classic concern confinement. Hooks and restic password helpers execute code; their apparently narrow sudo command names do not describe all possible effects. Sudoers argument wildcards can span whitespace.
- **Restoration and Redis:** restic `--path` selects a snapshot, while `--include` filters restored content. Restore dry-run may still lock the repository. Redis SCAN can return empty pages or duplicates, and COUNT is a hint; completeness depends on the cursor and changing keyspace. An application-stored encrypted password is not automatically a cracking-tool input.

Portable examples omit source credentials, flags, target addresses and one-off payloads. Artificial also contains differing target addresses in its setup text; no address was inferred from that inconsistency. Primary manuals and implementations are linked in each accepted package. These checks establish documented semantics, not successful Linux execution or universal support in historical versions.

## Reviewed material not turned into skills

| Material | Decision and remaining work |
|---|---|
| Arkham's GreatSCT payload, AV bypass and Windows UAC/DLL sequence | Windows-specific execution/evasion chain, not a reusable Linux utility procedure. No generic bypass recipe was copied. The final elevated account context does not by itself establish SYSTEM. |
| Armageddon's Drupal exploit and historical malicious snap construction | Application/version-specific exploitation and package authoring need their own fixtures. Snap inspection, hooks and mode semantics were retained; the old build script was not promoted to a general package recipe. |
| Artificial's TensorFlow Lambda upload and Backrest application chain | Kept the reproducible environment, file-format and restic lessons. Model loading and upload-trigger behavior require a controlled application/version fixture before a broader methodology can claim coverage. |
| Atlas's JD-GUI/dnSpy/WinSSHTerm analysis and decryption program | Reviewed all pages, including key derivation, byte-prefix handling and padding. These depend on the observed application build; hardcoded prefix lengths or slicing a fixed number of padding bytes are not universal cryptographic procedures. A Linux CLI decompiler skill needs an independently documented workflow. |
| Atom's Electron updater payload and application-specific DES recovery | The source explicitly uses a lab with Defender disabled. That does not establish generic payload success. Digest encoding was retained; the updater exploit and hardcoded decryption behavior require exact application/version fixtures. |
| Repeated Nmap, FTP, SSH, curl, file-copy, PowerShell and payload-handler commands | Existing coverage was checked. Simple commands without a new decision or failure lesson do not warrant more skill prose. Native Windows utilities are source context, not standalone Linux skills. |

All five PDFs are processed; these are deliberate scope decisions, not unread documents.

## Source fingerprints

SHA-256 identifies the exact originals even after the ignored inbox is replaced.

| File | SHA-256 |
|---|---|
| Arkham.pdf | `8c811274d8c100bba0b3cc75f830bbb063b4af65206129a5a6fd4f80cdc6ea40` |
| Armageddon.pdf | `8409f58d252c7bb97d9af51a4449456a74c65be745fb1eb9a032323c4bc020df` |
| Artificial.pdf | `c6f0a324fe68d5d9f8ed93b84b8dc1f80e085ef4c091e0d0257d850c0b12d833` |
| Atlas.pdf | `b6b337d1ceaf0bd750949f5f85ca3163b5dc52b3f15100962aa84c5ead19e438` |
| Atom.pdf | `b564f44d9a808edb87f6ab0ba0b41ac186f0da4c2fe80e7742f18638722b48a1` |

See the [validation record](validation.md) for checks actually executed. The [Linux adaptation guide](../GETTING_STARTED.md#2-adapt-to-this-machine) remains the next step for installed-help review and relevant success/failure fixtures. No change to GDB or the existing assessment methodology was needed.
