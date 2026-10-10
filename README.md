# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills supply tool selection and on-demand operational knowledge for capable CLI agents on the Linux distribution/image we deploy and control. A later pass on that image will add verified binary paths and relevant environment facts to the references. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [7z](skills/7z/SKILL.md) | Inspect archives and supported disk-image layers; distinguish format, encryption and integrity limitations. |
| [adb](skills/adb/SKILL.md) | Inspect a selected Android device and separate reverse routing, transfer privileges, proxy settings and CA trust. |
| [ansible-vault](skills/ansible-vault/SKILL.md) | Extract and decrypt vault objects without loading playbooks or confusing vault passwords with plaintext values. |
| [apktool](skills/apktool/SKILL.md) | Decode APK resources, resolve framework gaps and distinguish a rebuild from valid Android signing. |
| [aureport](skills/aureport/SKILL.md) | Interpret existing TTY audit records and correlate events without misattributing copied logs. |
| [awk](skills/awk/SKILL.md) | Separate program source, literal data and regexes; recognize quoted CSV and binary-transfer limits. |
| [aws](skills/aws/SKILL.md) | Inspect explicit S3/DynamoDB endpoints, bound reads and interpret pagination, object keys and composite keys. |
| [backy](skills/backy/SKILL.md) | Run an archive-only JSON task and distinguish skipped cycles, destructive sync options and verified backup output. |
| [base64](skills/base64/SKILL.md) | Preserve transferred bytes and distinguish digest bytes, base64url and HTTP form-encoding layers. |
| [bash](skills/bash/SKILL.md) | Diagnose startup, restricted sessions, pattern comparisons, data reparsing, environment inheritance and redirection order. |
| [bmap](skills/bmap/SKILL.md) | Inspect trailing filesystem slack with the legacy reader while preserving allocation and qualifying recovery evidence. |
| [bloodhound-python](skills/bloodhound-python/SKILL.md) | Choose CE/legacy collectors, scope collection and distinguish graph rights from current access. |
| [cast](skills/cast/SKILL.md) | Read Ethereum blocks, transactions and contract getters; distinguish ABI/state evidence from published transactions. |
| [certipy](skills/certipy/SKILL.md) | Collect AD CS evidence; interpret enrollment-agent and missing-SID conditions, issuance errors and mapping requirements. |
| [cewl](skills/cewl/SKILL.md) | Collect scoped website vocabulary with deliberate depth, filtering and plain-word output for offline audits. |
| [chisel](skills/chisel/SKILL.md) | Map normal/reverse forwards and SOCKS direction, explicit listeners and authenticated tunnel cleanup. |
| [consul](skills/consul/SKILL.md) | Inspect selected KV data, distinguish ACL permissions and validate configuration before reload decisions. |
| [cp](skills/cp/SKILL.md) | Copy selected directories and diagnose path, permission and metadata-preservation differences. |
| [cryptsetup](skills/cryptsetup/SKILL.md) | Inspect and unlock LUKS image copies with read-only mappings and filesystem-aware mounting. |
| [curl](skills/curl/SKILL.md) | Preserve HTTP/cache evidence; construct API/GraphQL requests, inspect partial results and distinguish proxy forwarding, CONNECT and bypass rules. |
| [dd](skills/dd/SKILL.md) | Extract measured image byte ranges without hardcoded header sizes, overwrite or unnoticed short copies. |
| [derby-ij](skills/derby-ij/SKILL.md) | Inspect consistent Derby copies with embedded JDBC, schema discovery, bounded SQL and understood display/lock limits. |
| [diff](skills/diff/SKILL.md) | Compare acquired trees against a matching baseline and distinguish content changes from incomplete comparisons. |
| [dig](skills/dig/SKILL.md) | Query explicit DNS servers and compare authoritative, cached, negative and application resolver views. |
| [dirsearch](skills/dirsearch/SKILL.md) | Discover scoped web paths; narrow partial-name candidates and handle expansion, soft 404s and redirects. |
| [dive](skills/dive/SKILL.md) | Inspect local image layers, distinguish deletion markers and recover selected historical file bytes. |
| [docker](skills/docker/SKILL.md) | Reproduce pinned environments; interpret daemon authority, mounts/environment fields and image versus filesystem archives. |
| [dotnet](skills/dotnet/SKILL.md) | Distinguish .NET Framework/platform targets, select SDK/runtime context and build or run reviewed projects explicitly. |
| [dpkg-query](skills/dpkg-query/SKILL.md) | Match file ownership, installed state and complete Debian/Ubuntu package versions to the applicable vendor advisory. |
| [ebook-convert](skills/ebook-convert/SKILL.md) | Convert e-books with explicit formats and diagnose resource inclusion and transformation stages. |
| [evil-winrm](skills/evil-winrm/SKILL.md) | Establish WinRM sessions, inspect current token authority and diagnose transport, access and transfer issues. |
| [exiftool](skills/exiftool/SKILL.md) | Read image/document metadata while preserving tag groups and treating identities as leads. |
| [feroxbuster](skills/feroxbuster/SKILL.md) | Bound web discovery and interpret wildcard filters, parent-directory denial, accessible children and incomplete scans. |
| [ffuf](skills/ffuf/SKILL.md) | Compare paths/vhosts with bounded requests, method context, measured baselines and understood filters. |
| [fickling](skills/fickling/SKILL.md) | Inspect pickle streams statically and distinguish findings, scanner failures and incomplete model coverage. |
| [file](skills/file/SKILL.md) | Classify artifacts without confusing format labels, managed assemblies, transfer integrity and runtime compatibility. |
| [find](skills/find/SKILL.md) | Scope searches and timestamp inventories while interpreting permissions, emptiness, traversal errors and action boundaries. |
| [findmnt](skills/findmnt/SKILL.md) | Identify covering filesystems and exact mountpoints while preserving namespace and host-source uncertainty. |
| [firefox-decrypt](skills/firefox-decrypt/SKILL.md) | Recover saved logins from one authorized offline Mozilla profile; diagnose key/NSS compatibility and incomplete records. |
| [forge](skills/forge/SKILL.md) | Diagnose Foundry builds with explicit project/compiler context and correctly interpreted helper trace logs. |
| [ftp](skills/ftp/SKILL.md) | Transfer selected files, diagnose data channels and verify an authorised upload-to-web mapping without inferring code execution. |
| [gdb](skills/gdb/SKILL.md) | Follow native core frames/state to a bounded diagnosis, or inspect a controlled live reproduction. |
| [gdbserver](skills/gdbserver/SKILL.md) | Debug controlled remote programs over SSH with understood transport, connection modes and process lifetime. |
| [getcap](skills/getcap/SKILL.md) | Verify file capabilities and distinguish stored flags, execution conditions and current process authority. |
| [getfacl](skills/getfacl/SKILL.md) | Explain POSIX ACL masks, named identities, parent traversal and default inheritance for access failures. |
| [git](skills/git/SKILL.md) | Inspect history, stored links/submodules and remote URLs; check scoped patches and diagnose local hooks. |
| [git-dumper](skills/git-dumper/SKILL.md) | Recover exposed Git data within an isolated environment and distinguish missing objects, checkout failures and incomplete history. |
| [go](skills/go/SKILL.md) | Build reviewed CLI projects; resolve generated imports and distinguish command construction, execution and unchecked results. |
| [gobuster](skills/gobuster/SKILL.md) | Choose web discovery modes and interpret wildcard, redirect, method and validation responses. |
| [gpp-decrypt](skills/gpp-decrypt/SKILL.md) | Decode captured GPP cpassword values; distinguish the Ruby and Python implementations. |
| [grafana2hashcat](skills/grafana2hashcat/SKILL.md) | Convert and verify compatible Grafana records; distinguish malformed input, wrong encodings and recovery. |
| [grep](skills/grep/SKILL.md) | Filter literal or regex text while preserving alternative/combined conditions, binary handling and error evidence. |
| [h2csmuggler](skills/h2csmuggler/SKILL.md) | Distinguish h2c upgrade acceptance, tunneled application replies and actual access-control differences. |
| [hashcat](skills/hashcat/SKILL.md) | Check application/Gitea PBKDF2, sha512crypt, salted MD5/SHA-1, Ansible Vault and NT/Kerberos records or binary containers with correct input and recovery handling. |
| [hashid](skills/hashid/SKILL.md) | Identify candidate hash formats offline and handle ambiguous matches, unsupported prefixes and format hints. |
| [httpie](skills/httpie/SKILL.md) | Construct JSON API requests offline and interpret selected lookups with explicit input and status handling. |
| [iconv](skills/iconv/SKILL.md) | Convert captured text with explicit encodings; distinguish UTF-16 byte order, terminators and lossy recovery. |
| [iis-shortname-scanner](skills/iis-shortname-scanner/SKILL.md) | Check IIS short-name disclosure and distinguish partial aliases, response ambiguity and confirmed full paths. |
| [ike-scan](skills/ike-scan/SKILL.md) | Interpret an IKE endpoint's initial proposal response, notify errors and vendor fingerprints without claiming authentication. |
| [ilspycmd](skills/ilspycmd/SKILL.md) | Inspect .NET types, time-seeded crypto, serialization and archive-write paths without launching the assembly. |
| [impacket-dacledit](skills/impacket-dacledit/SKILL.md) | Inspect selected AD DACLs, trustee filters, inheritance and the limited scope of ACL backups. |
| [impacket-getadusers](skills/impacket-getadusers/SKILL.md) | Query selected AD user metadata and interpret filtering, email requirements and DC-local logon dates. |
| [impacket-getnpusers](skills/impacket-getnpusers/SKILL.md) | Check selected accounts for AS-REP material without password guessing. |
| [impacket-getst](skills/impacket-getst/SKILL.md) | Request selected Kerberos service tickets and interpret SPNs, existing delegation and saved cache identity. |
| [impacket-gettgt](skills/impacket-gettgt/SKILL.md) | Obtain and select a Kerberos file cache using known credentials. |
| [impacket-getuserspns](skills/impacket-getuserspns/SKILL.md) | Separate SPN enumeration from selected service-ticket requests for an offline audit. |
| [impacket-lookupsid](skills/impacket-lookupsid/SKILL.md) | Resolve bounded RID ranges while preserving SID scope, principal types and incomplete-lookup evidence. |
| [impacket-mssqlclient](skills/impacket-mssqlclient/SKILL.md) | Inspect SQL Server authentication, cache/SPN selection, SQL identity and command-execution configuration. |
| [impacket-reg](skills/impacket-reg/SKILL.md) | Query selected remote registry keys while accounting for hive context and service-state changes. |
| [impacket-rpcmap](skills/impacket-rpcmap/SKILL.md) | Distinguish scoped RPC interface binding, automatic fallback probes and actual method calls. |
| [impacket-secretsdump](skills/impacket-secretsdump/SKILL.md) | Parse SAM/SECURITY/NTDS snapshots or audit selected-account replication while retaining credential-store identity. |
| [impacket-smbserver](skills/impacket-smbserver/SKILL.md) | Run a temporary bound SMB transfer share with explicit authentication and verified file transfer. |
| [impacket-ticketer](skills/impacket-ticketer/SKILL.md) | Prepare bounded lab service-ticket fixtures with explicit keys, identity, lifetime and cache interpretation. |
| [ip](skills/ip/SKILL.md) | Explain Linux route selection using local addresses, policy rules, prefix specificity and namespace-aware lookups. |
| [ipcs](skills/ipcs/SKILL.md) | Inspect System V shared-memory metadata, keys, segment IDs, permissions and namespace limits. |
| [ipfs](skills/ipfs/SKILL.md) | Inspect local Kubo blocks, resolve UnixFS roots and recover selected files without fetching from peers. |
| [iptables](skills/iptables/SKILL.md) | Inspect firewall backend, family and packet path with ordered rules, state, source/destination ports and saved-versus-live limits. |
| [iptables-save](skills/iptables-save/SKILL.md) | Capture ruleset evidence while distinguishing output-file effects, coverage, restore and persistence. |
| [jadx](skills/jadx/SKILL.md) | Inspect APK resources and DEX call paths while recovering from incomplete decompilation. |
| [jarsigner](skills/jarsigner/SKILL.md) | Interpret JAR signature coverage, unsigned zero exits, strict warnings and Android verifier boundaries. |
| [jdb](skills/jdb/SKILL.md) | Attach to a JVM, reach relevant breakpoints and inspect suspended frames with understood evaluation effects. |
| [jenkins-cli](skills/jenkins-cli/SKILL.md) | Verify controller identity/permissions and inspect an existing build log; distinguish transports, local authentication files and historical disclosure evidence. |
| [john](skills/john/SKILL.md) | Run bounded Jumbo checks on NT/NetNTLMv2/AS-REP, ZIP, KeePass with key files, OpenPGP secret keys, bcrypt, phpass, raw MD5/SHA-256 and HS256 JWT artifacts. |
| [jq](skills/jq/SKILL.md) | Validate JSON types, preserve text, serialize requests and distinguish config transformations from path validation. |
| [jwt-tool](skills/jwt-tool/SKILL.md) | Inspect JWT fixtures, claim mappings and verification limits; distinguish tokens from browser storage and application sessions. |
| [keepassxc-cli](skills/keepassxc-cli/SKILL.md) | Inspect a database with known unlock factors and retrieve exact entries/fields without broad disclosure. |
| [kerbrute](skills/kerbrute/SKILL.md) | Check a bounded candidate username list against a selected KDC and interpret incomplete results. |
| [kinit](skills/kinit/SKILL.md) | Obtain MIT Kerberos tickets in an explicit cache, including existing-certificate PKINIT. |
| [ldapsearch](skills/ldapsearch/SKILL.md) | Query AD identities, deleted objects, SPNs and lockout policies with correct authentication and coverage. |
| [ldbsearch](skills/ldbsearch/SKILL.md) | Inspect offline SSSD cache records with DN/attribute context and distinguish missing, stale and unparseable evidence. |
| [linpeas](skills/linpeas/SKILL.md) | Scope enumeration checks and verify unfamiliar SUID helpers, execution conditions and vendor package evidence. |
| [logrotate](skills/logrotate/SKILL.md) | Preview actual rotation jobs and interpret state, skip conditions, permissions and hook identities. |
| [mail](skills/mail/SKILL.md) | Distinguish GNU Mailutils and S-nail flags, subject handling, attachments and submission evidence. |
| [marshalsec](skills/marshalsec/SKILL.md) | Select unmarshalling fixtures and distinguish local test execution, JNDI stages and runtime dependencies. |
| [masscan](skills/masscan/SKILL.md) | Discover scoped TCP listeners with explicit configuration and host/protocol-preserving service follow-up. |
| [mdbtools](skills/mdbtools/SKILL.md) | Inventory and export selected Access database tables without corrupting field interpretation. |
| [mount-cifs](skills/mount-cifs/SKILL.md) | Mount SMB shares read-only; distinguish metadata timestamps, dialects, signing and local/server permissions. |
| [mount-nfs](skills/mount-nfs/SKILL.md) | Mount selected NFS exports read-only; diagnose version, identity, locking and mount-state evidence. |
| [msf-pattern](skills/msf-pattern/SKILL.md) | Pair Metasploit pattern generation and offset lookup without confusing heuristic matches or overwritten fields. |
| [mysql](skills/mysql/SKILL.md) | Diagnose connections and string comparisons; inspect native function metadata and distinguish client/server execution and file access. |
| [mysqldump](skills/mysqldump/SKILL.md) | Back up a selected database and distinguish SQL failures, compression integrity, object coverage and validated recovery. |
| [ncat](skills/ncat/SKILL.md) | Interpret TCP line protocols, Memcached slab counts and selected values with correct framing and timeout handling. |
| [netexec](skills/netexec/SKILL.md) | Control known credential pairs; interpret user metadata, password/share results and LDAP machine-account quota. |
| [nginx](skills/nginx/SKILL.md) | Inspect selected configuration, worker/file authority, WebDAV conditions and validation-versus-live-state evidence. |
| [nmap](skills/nmap/SKILL.md) | Keep protocol, address and IPsec vantage explicit; interpret service probes and uncertain states. |
| [npbackup-cli](skills/npbackup-cli/SKILL.md) | Select exact backup snapshots, recover a file and distinguish backend writes from wrapper policy/status failures. |
| [oathtool](skills/oathtool/SKILL.md) | Generate known-secret TOTP and diagnose encoding, parameter and clock mismatches. |
| [objdump](skills/objdump/SKILL.md) | Inspect headers and bounded disassembly while separating bytes, source lines and runtime evidence. |
| [openssl](skills/openssl/SKILL.md) | Inspect certificates, key formats and TLS mail sessions; recover known-format AES-CBC artifacts with explicit byte/padding interpretation. |
| [pacman](skills/pacman/SKILL.md) | Inspect Arch package metadata, payloads, scriptlets and ownership before choosing an installation transaction. |
| [pd4cmd](skills/pd4cmd/SKILL.md) | Convert reviewed HTML with PD4ML; diagnose entrypoints, resource access, layout and stale PDF output. |
| [php](skills/php/SKILL.md) | Inspect PHP configuration, execution syntax, extensions, PHARs, output encoding, dynamic SQL fields and upload validation. |
| [pip](skills/pip/SKILL.md) | Compare manifest and installed versions; match interpreter/wheel compatibility and control dependency/build fallback. |
| [proxychains](skills/proxychains/SKILL.md) | Route compatible TCP clients with explicit SOCKS/HTTP CONNECT context and verified DNS/transport limits. |
| [ps](skills/ps/SKILL.md) | Inspect process identity/state and targeted procfs evidence without confusing NUL-separated or mutable metadata. |
| [ps2pdf](skills/ps2pdf/SKILL.md) | Convert reviewed PostScript and diagnose status, template errors and Ghostscript file-access controls. |
| [pspy](skills/pspy/SKILL.md) | Correlate short-lived processes with jobs/actions while retaining exact paths, identities and visibility limits. |
| [psql](skills/psql/SKILL.md) | Establish PostgreSQL identity, inspect schemas and export bounded rows with explicit quoting and failure handling. |
| [pwntools](skills/pwntools/SKILL.md) | Complete framed exchanges, interpret timeouts/EOF and reconstruct integer fields with explicit widths and byte order. |
| [pygpoabuse](skills/pygpoabuse/SKILL.md) | Plan isolated lab GPO task tests with explicit commands, client scope, before-state and incomplete-cleanup handling. |
| [pypykatz](skills/pypykatz/SKILL.md) | Inspect LSASS snapshots and derive known-password NT values while preserving identity and artifact type. |
| [python-http-server](skills/python-http-server/SKILL.md) | Serve a dedicated directory temporarily and interpret transfer/callback evidence. |
| [python3](skills/python3/SKILL.md) | Inspect source without imports; trace evaluation, separate child output/status, diagnose bytes and decode SAML Redirect requests. |
| [rdate](skills/rdate/SKILL.md) | Diagnose clock skew with print-only SNTP queries and distinguish protocol, timezone and synchronization issues. |
| [readelf](skills/readelf/SKILL.md) | Map ELF layouts and inspect dynamic dependencies/symbols while separating artifact metadata from runtime behavior. |
| [readpst](skills/readpst/SKILL.md) | Convert PST/supported OST mail while accounting for MIME, image attachments and conversion limits. |
| [redis-cli](skills/redis-cli/SKILL.md) | Inspect selected Redis values with known authentication, explicit databases and bounded cursor scans. |
| [responder](skills/responder/SKILL.md) | Separate name observation from active authentication listeners and preserve complete capture evidence. |
| [restic](skills/restic/SKILL.md) | Select backup snapshots/paths and restore into a new directory with understood helpers, filters and locks. |
| [ropgadget](skills/ropgadget/SKILL.md) | Inspect gadget candidates with understood search depth, address filters and complete instruction effects. |
| [rsync](skills/rsync/SKILL.md) | Inspect daemon modules and retrieve a selected file with explicit transport, destination and partial-copy handling. |
| [samdump2](skills/samdump2/SKILL.md) | Extract matching legacy SAM/SYSTEM records and detect unsupported formats or misleading empty-password values. |
| [scp](skills/scp/SKILL.md) | Transfer selected files and recover from authentication, SFTP-subsystem, path or partial-copy failures. |
| [screen](skills/screen/SKILL.md) | Identify and resume sessions with understood sharing, ownership, terminal and multiuser requirements. |
| [script](skills/script/SKILL.md) | Allocate a util-linux PTY or capture a terminal session with correct exit/logging semantics. |
| [searchsploit](skills/searchsploit/SKILL.md) | Search and inspect local exploit candidates without confusing title matches with applicability. |
| [sendmail](skills/sendmail/SKILL.md) | Submit requested messages with explicit envelope recipients and distinguish queue acceptance from delivery. |
| [showmount](skills/showmount/SKILL.md) | Inspect NFS export advertisements while distinguishing MOUNT-service limits, NFSv4 and actual access. |
| [smbclient](skills/smbclient/SKILL.md) | Retrieve selected SMB files with explicit identity and distinguish share labels, file permissions and execution evidence. |
| [smbmap](skills/smbmap/SKILL.md) | Inventory SMB access without default write probes and control traversal and selected downloads. |
| [smbpasswd](skills/smbpasswd/SKILL.md) | Change a known account's remote SMB password while distinguishing required changes, resets and local database operations. |
| [smtp-user-enum](skills/smtp-user-enum/SKILL.md) | Compare scoped SMTP recipient responses without treating tool classifications as mailbox proof. |
| [snap](skills/snap/SKILL.md) | Inspect revisions, confinement and change tasks; distinguish signature checks from executable install hooks. |
| [snmpwalk](skills/snmpwalk/SKILL.md) | Query bounded OIDs, distinguish contact text from credentials and load hardware inventory guidance on demand. |
| [sqlite3](skills/sqlite3/SKILL.md) | Inspect database copies, preserve encoded-field identity and handle query ordering and WAL sidecars. |
| [sqlmap](skills/sqlmap/SKILL.md) | Test a selected HTTP parameter and inspect scoped database metadata or samples with request/session fidelity. |
| [ss](skills/ss/SKILL.md) | Inspect actual listeners/connections, address families, process visibility and namespaces. |
| [ssh](skills/ssh/SKILL.md) | Forward loopback services, diagnose tunnel failures and account for local execution during configuration evaluation. |
| [ssh-keygen](skills/ssh-keygen/SKILL.md) | Derive public keys and compare fingerprints while preserving private artifacts and format distinctions. |
| [strace](skills/strace/SKILL.md) | Trace file/network failures and interpret acquired reads with process, descriptor, byte-count and tracing-side-effect context. |
| [strings](skills/strings/SKILL.md) | Extract binary text with offsets/alternate encodings; retain record context before assigning database values to accounts. |
| [strongswan-ipsec](skills/strongswan-ipsec/SKILL.md) | Inspect existing VPN SAs and diagnose selector, transport-mode and application-path mismatches. |
| [sudo](skills/sudo/SKILL.md) | Interpret RunAs, PAM, helper paths/working directories, environment handling and sudoedit copy-back. |
| [swaks](skills/swaks/SKILL.md) | Preview MIME and diagnose explicit SMTP stages, TLS verification and delivery evidence. |
| [tar](skills/tar/SKILL.md) | Extract selected members; distinguish source paths, stored names, restored ownership and partial/sidecar consistency. |
| [tcpdump](skills/tcpdump/SKILL.md) | Capture scoped traffic at the correct interface/port, retain handshake evidence and distinguish application conclusions. |
| [text2wave](skills/text2wave/SKILL.md) | Generate speech fixtures while separating text normalization, audio output and downstream recognition. |
| [thrift](skills/thrift/SKILL.md) | Generate reviewed RPC bindings and distinguish compiler, transport, protocol and handler outcomes. |
| [tshark](skills/tshark/SKILL.md) | Correlate saved FTP/TLS/Kerberos traffic with conversation identity, pre-authentication fields and incomplete evidence. |
| [unzip](skills/unzip/SKILL.md) | Inspect ZIP names and CRCs; recover selected members while distinguishing path, collision and partial-output behavior. |
| [vim](skills/vim/SKILL.md) | Control startup/modelines and recover copied swap artifacts with understood completeness limits. |
| [vtysh](skills/vtysh/SKILL.md) | Diagnose FRR/Quagga BGP sessions, prefix selection and advertisement policy against forwarding evidence. |
| [wfuzz](skills/wfuzz/SKILL.md) | Compare HTTP hosts/parameters with baselines, response filters, bounded ID ranges and known session state. |
| [windapsearch](skills/windapsearch/SKILL.md) | Inspect AD users/custom attributes with legacy Python syntax and correct visibility, encoding and exit-status interpretation. |
| [wpscan](skills/wpscan/SKILL.md) | Scope WordPress plugin/user inventory and distinguish detection, account access and incomplete vulnerability evidence. |
| [xml-pp](skills/xml-pp/SKILL.md) | Format trusted XML while retaining original bytes, parse failures and entity-handling limits. |
| [xxd](skills/xxd/SKILL.md) | Inspect and reconstruct exact bytes; distinguish offsets, patching, hex representation and text encoding. |
| [ysoserial](skills/ysoserial/SKILL.md) | Generate selected Java serialization fixtures without confusing producer failures, binary output and target effects. |

The accepted skills are documentation-reviewed but have not been executed or evaluated with an agent on Linux. See the [validation record](docs/validation.md). Source coverage, corrections and deferred candidates are recorded for [batch 1](docs/ctf-writeups-ingestion.md), [batch 2](docs/ctf-writeups-batch2.md), [batch 3](docs/ctf-writeups-batch3.md), [batch 4](docs/ctf-writeups-batch4.md), [batch 5](docs/ctf-writeups-batch5.md), [batch 6](docs/ctf-writeups-batch6.md), [batch 7](docs/ctf-writeups-batch7.md), [batch 8](docs/ctf-writeups-batch8.md) and the [overnight intake](docs/ctf-writeups-overnight-2026-10-10.md).

## Simple structure

~~~text
skills/<tool>/
    SKILL.md                   # metadata and working instructions
    references/                # optional conditional working guidance

authoring/                     # schema, prompts and optional templates
docs/                          # source/intake records, setup and validation history
ingest/                        # local source documents, ignored by Git
evaluation/                    # optional test design and case template
scripts/                       # help capture and repository checker
tests/
profile/                       # optional shell settings
~~~

One `SKILL.md` is enough for a small skill. Use ordinary Markdown with the standard [Agent Skills frontmatter](https://agentskills.io/specification). Add references for substantial conditional working detail or scripts for useful repeated execution. Required resources stay inside their own skill folder. Review dates, full source trails and test history live in `docs/`; keep actionable compatibility conditions and useful documentation links in the worker instructions.

## Create or improve a skill

1. Choose a task or known mistake. Collect practical documentation, examples or transcripts using the [source guide](authoring/sources.md).
2. Use the [authoring prompt](authoring/create-skill.prompt.md) and [schema](authoring/schema.md). The [single template](authoring/skill.template.md) is optional. Identify the capability gap against existing coverage; a short correction may be enough.
3. Connect commands, relevant results, interpretation and the next decision where examples help. Label invented output as illustrative. Review accuracy, scope and repetition with the [review prompt](authoring/review-skill.prompt.md); the [evaluation guide](evaluation/README.md) covers actual worker comparisons.
4. Add accepted skills to the catalogue above. Keep drafts/raw sources in ignored `work/` and test artifacts in `runs/`. Record source-to-skill mappings and test results in the intake/validation records; workers need only their selected skill folders.

Put required task instructions and resource navigation near the start; keep conditional references selective. See the [first-read rationale](docs/harnesses.md#skill-loading-and-the-first-read) and [authoring rules](authoring/schema.md).

The [operational knowledge review](docs/operational-skills-review-2026-10-10.md) explains schema v0.7: concise tool selection, conditional task references, later controlled-image path enrichment and incremental conformity during ingestion. Existing skills migrate when revisited; the whole library has not yet been audited.

Commands, interpretations and recovery advice need evidence. Documentation review, procedure execution and improved agent performance are different claims. Record only what was actually established.

## Repository checks

~~~bash
python3 scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
~~~

These validate links, basic frontmatter, standalone packaging and helper behaviour. Linux tool execution and worker usefulness need separate checks. Compare successful outcomes, recovery and total task cost against a baseline.

`AGENTS.md` and `CLAUDE.md` are for authors maintaining this repository. Workers need selected skill folders only. Optional settings in `profile/` are separate from skill installation. Add a repository license when you choose distribution terms.
