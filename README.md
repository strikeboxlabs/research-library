# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills add useful tool knowledge for agents that already use the CLI competently. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [7z](skills/7z/SKILL.md) | Inspect, test and extract archives; distinguish unsupported encryption from password or integrity failures. |
| [ansible-vault](skills/ansible-vault/SKILL.md) | Extract and decrypt vault objects without loading playbooks or confusing vault passwords with plaintext values. |
| [aureport](skills/aureport/SKILL.md) | Interpret existing TTY audit records and correlate events without misattributing copied logs. |
| [awk](skills/awk/SKILL.md) | Separate program source, literal data and regexes; recognize quoted CSV and binary-transfer limits. |
| [base64](skills/base64/SKILL.md) | Preserve transferred bytes and distinguish raw digests, ordinary base64 and unpadded base64url. |
| [bash](skills/bash/SKILL.md) | Diagnose startup, effective-ID handling, environment inheritance and redirection order in scripts/jobs. |
| [bloodhound-python](skills/bloodhound-python/SKILL.md) | Choose CE/legacy collectors, scope directory collection and diagnose authentication/import gaps. |
| [certipy](skills/certipy/SKILL.md) | Collect AD CS directory evidence and distinguish template findings, omitted CA checks and current mapping requirements. |
| [chisel](skills/chisel/SKILL.md) | Map normal/reverse forwards and SOCKS direction, explicit listeners and authenticated tunnel cleanup. |
| [consul](skills/consul/SKILL.md) | Inspect selected KV data, distinguish ACL permissions and validate configuration before reload decisions. |
| [cryptsetup](skills/cryptsetup/SKILL.md) | Inspect and unlock LUKS image copies with read-only mappings and filesystem-aware mounting. |
| [curl](skills/curl/SKILL.md) | Preserve HTTP evidence, construct API requests and distinguish proxy forwarding, CONNECT and bypass rules. |
| [dd](skills/dd/SKILL.md) | Extract measured image byte ranges without hardcoded header sizes, overwrite or unnoticed short copies. |
| [dirsearch](skills/dirsearch/SKILL.md) | Discover scoped web paths; handle wordlist expansion, soft 404s, redirects and incomplete scans. |
| [docker](skills/docker/SKILL.md) | Reproduce pinned tool environments with explicit bind mounts, ownership, network and runtime boundaries. |
| [dotnet](skills/dotnet/SKILL.md) | Select SDK/runtime context and build or run reviewed projects with explicit restore and launch behavior. |
| [evil-winrm](skills/evil-winrm/SKILL.md) | Establish WinRM sessions with known credentials and diagnose transport, access and transfer issues. |
| [exiftool](skills/exiftool/SKILL.md) | Read image/document metadata while preserving tag groups and treating identities as leads. |
| [ffuf](skills/ffuf/SKILL.md) | Compare paths/vhosts with bounded requests, method context, measured baselines and understood filters. |
| [file](skills/file/SKILL.md) | Classify artifacts without confusing format labels, managed assemblies, transfer integrity and runtime compatibility. |
| [find](skills/find/SKILL.md) | Scope file searches and interpret emptiness, traversal errors, predicate grouping and action boundaries. |
| [ftp](skills/ftp/SKILL.md) | Retrieve selected binary files, distinguish client-specific HTTP fetching and diagnose data-channel failures. |
| [gdb](skills/gdb/SKILL.md) | Examine matching native cores or controlled live instruction/memory state with explicit address and ASLR context. |
| [gdbserver](skills/gdbserver/SKILL.md) | Debug controlled remote programs over SSH with understood transport, connection modes and process lifetime. |
| [git](skills/git/SKILL.md) | Inspect historical file content and renames without changing the checkout. |
| [go](skills/go/SKILL.md) | Build reviewed CLI projects with explicit module, toolchain, dependency-change and target context. |
| [gobuster](skills/gobuster/SKILL.md) | Choose web discovery modes and interpret wildcard, redirect, method and validation responses. |
| [gpp-decrypt](skills/gpp-decrypt/SKILL.md) | Decode captured GPP cpassword values; distinguish the Ruby and Python implementations. |
| [grep](skills/grep/SKILL.md) | Filter literal or regex text while preserving alternative/combined conditions, binary handling and error evidence. |
| [hashcat](skills/hashcat/SKILL.md) | Check application, Ansible Vault and NT/Kerberos records or binary containers with correct input and recovery handling. |
| [ilspycmd](skills/ilspycmd/SKILL.md) | Inspect .NET types and property/serialization paths from Linux without launching the inspected assembly. |
| [impacket-getnpusers](skills/impacket-getnpusers/SKILL.md) | Check selected accounts for AS-REP material without password guessing. |
| [impacket-getst](skills/impacket-getst/SKILL.md) | Request selected Kerberos service tickets and interpret SPNs, existing delegation and saved cache identity. |
| [impacket-gettgt](skills/impacket-gettgt/SKILL.md) | Obtain and select a Kerberos file cache using known credentials. |
| [impacket-getuserspns](skills/impacket-getuserspns/SKILL.md) | Separate SPN enumeration from selected service-ticket requests for an offline audit. |
| [impacket-reg](skills/impacket-reg/SKILL.md) | Query selected remote registry keys while accounting for hive context and service-state changes. |
| [impacket-rpcmap](skills/impacket-rpcmap/SKILL.md) | Distinguish scoped RPC interface binding, automatic fallback probes and actual method calls. |
| [impacket-secretsdump](skills/impacket-secretsdump/SKILL.md) | Parse SAM/NTDS snapshots or audit selected-account replication while retaining credential-store identity. |
| [impacket-smbserver](skills/impacket-smbserver/SKILL.md) | Run a temporary bound SMB transfer share with explicit authentication and verified file transfer. |
| [iptables](skills/iptables/SKILL.md) | Inspect the selected firewall backend, family, table and chain with understood ordering, counters and live mutations. |
| [iptables-save](skills/iptables-save/SKILL.md) | Capture ruleset evidence while distinguishing output-file effects, coverage, restore and persistence. |
| [jdb](skills/jdb/SKILL.md) | Attach to a JVM, reach relevant breakpoints and inspect suspended frames with understood evaluation effects. |
| [john](skills/john/SKILL.md) | Run bounded Jumbo checks on NT/NetNTLMv2/AS-REP, ZIP, raw SHA-256 and original HS256 JWT artifacts. |
| [jq](skills/jq/SKILL.md) | Validate JSON types, preserve returned text and serialize requests while recognizing upstream text transformations. |
| [jwt-tool](skills/jwt-tool/SKILL.md) | Inspect and modify local JWT fixtures with explicit algorithms, key bytes and verification limits. |
| [kerbrute](skills/kerbrute/SKILL.md) | Check a bounded candidate username list against a selected KDC and interpret incomplete results. |
| [kinit](skills/kinit/SKILL.md) | Obtain MIT Kerberos tickets in an explicit cache, including existing-certificate PKINIT. |
| [ldapsearch](skills/ldapsearch/SKILL.md) | Query AD with correct authentication, bases/filters and paging while retaining identity and attribute coverage. |
| [linpeas](skills/linpeas/SKILL.md) | Scope enumeration checks, account for authentication/network effects and verify highlighted permissions evidence. |
| [mail](skills/mail/SKILL.md) | Distinguish GNU Mailutils and S-nail flags, subject handling, attachments and submission evidence. |
| [marshalsec](skills/marshalsec/SKILL.md) | Select unmarshalling fixtures and distinguish local test execution, JNDI stages and runtime dependencies. |
| [mdbtools](skills/mdbtools/SKILL.md) | Inventory and export selected Access database tables without corrupting field interpretation. |
| [mount-cifs](skills/mount-cifs/SKILL.md) | Mount selected SMB shares read-only and distinguish dialect, authentication and local/server permissions. |
| [mysql](skills/mysql/SKILL.md) | Diagnose connection/account identity, run bounded batch queries and understand server/LOCAL file access. |
| [ncat](skills/ncat/SKILL.md) | Interact with simple TCP services and distinguish line endings, EOF and connection/idle timeouts. |
| [netexec](skills/netexec/SKILL.md) | Control known credential pairs and interpret password statuses, share probes and path-specific access. |
| [nmap](skills/nmap/SKILL.md) | Keep TCP/UDP and IPv4/IPv6 coverage explicit; interpret service probes and uncertain states. |
| [objdump](skills/objdump/SKILL.md) | Inspect headers and bounded disassembly while separating bytes, source lines and runtime evidence. |
| [openssl](skills/openssl/SKILL.md) | Inspect requests, certificates and PKCS#12 bundles while separating private keys, encodings, identity and trust. |
| [pip](skills/pip/SKILL.md) | Match interpreter, wheel ABI and platform while controlling dependency resolution and source-build fallback. |
| [proxychains](skills/proxychains/SKILL.md) | Route compatible TCP clients with explicit SOCKS/HTTP CONNECT context and verified DNS/transport limits. |
| [ps](skills/ps/SKILL.md) | Inspect process identity/state and targeted procfs evidence without confusing NUL-separated or mutable metadata. |
| [pspy](skills/pspy/SKILL.md) | Correlate short-lived processes with jobs/actions while retaining exact paths, identities and visibility limits. |
| [pygpoabuse](skills/pygpoabuse/SKILL.md) | Plan isolated lab GPO task tests with explicit commands, client scope, before-state and incomplete-cleanup handling. |
| [python-http-server](skills/python-http-server/SKILL.md) | Serve a dedicated directory temporarily and interpret transfer/callback evidence. |
| [readelf](skills/readelf/SKILL.md) | Map ELF headers, segments, symbols and section bytes without confusing file and runtime addresses. |
| [readpst](skills/readpst/SKILL.md) | Convert PST/supported OST mail while accounting for MIME, image attachments and conversion limits. |
| [redis-cli](skills/redis-cli/SKILL.md) | Inspect selected Redis values with known authentication, explicit databases and bounded cursor scans. |
| [restic](skills/restic/SKILL.md) | Select backup snapshots/paths and restore into a new directory with understood helpers, filters and locks. |
| [ropgadget](skills/ropgadget/SKILL.md) | Inspect gadget candidates with understood search depth, address filters and complete instruction effects. |
| [screen](skills/screen/SKILL.md) | Identify and resume sessions with understood sharing, ownership, terminal and multiuser requirements. |
| [script](skills/script/SKILL.md) | Allocate a util-linux PTY or capture a terminal session with correct exit/logging semantics. |
| [searchsploit](skills/searchsploit/SKILL.md) | Search and inspect local exploit candidates without confusing title matches with applicability. |
| [smbclient](skills/smbclient/SKILL.md) | Retrieve selected SMB files and distinguish share labels, file permissions, replacement and execution evidence. |
| [smbmap](skills/smbmap/SKILL.md) | Inventory SMB access without default write probes and control traversal and selected downloads. |
| [smbpasswd](skills/smbpasswd/SKILL.md) | Change a known account's remote SMB password while distinguishing required changes, resets and local database operations. |
| [smtp-user-enum](skills/smtp-user-enum/SKILL.md) | Compare scoped SMTP recipient responses without treating tool classifications as mailbox proof. |
| [snap](skills/snap/SKILL.md) | Inspect revisions, confinement and change tasks; distinguish signature checks from executable install hooks. |
| [snmpwalk](skills/snmpwalk/SKILL.md) | Query bounded SNMP subtrees/instances and distinguish timeout, coverage and BITS rendering. |
| [sqlite3](skills/sqlite3/SKILL.md) | Inspect existing databases with bounded queries, structured output and coherent WAL-sidecar handling. |
| [ss](skills/ss/SKILL.md) | Inspect actual listeners/connections, address families, process visibility and namespaces. |
| [ssh](skills/ssh/SKILL.md) | Forward loopback services, diagnose tunnel failures and account for local execution during configuration evaluation. |
| [ssh-keygen](skills/ssh-keygen/SKILL.md) | Derive public keys and compare fingerprints while preserving private artifacts and format distinctions. |
| [strace](skills/strace/SKILL.md) | Trace actual file/network operations and interpret config lookups and failed calls. |
| [strings](skills/strings/SKILL.md) | Extract binary text with file offsets and alternate encodings for evidence-led triage. |
| [sudo](skills/sudo/SKILL.md) | Interpret RunAs, PAM, runtime/file-writing capabilities, environment handling and sudoedit copy-back. |
| [swaks](skills/swaks/SKILL.md) | Preview MIME and diagnose explicit SMTP stages, TLS verification and delivery evidence. |
| [tar](skills/tar/SKILL.md) | Extract selected backup members and assess partial/nested recovery, permissions and sidecar consistency. |
| [tcpdump](skills/tcpdump/SKILL.md) | Capture scoped traffic and distinguish packet evidence from application-level conclusions. |
| [text2wave](skills/text2wave/SKILL.md) | Generate speech fixtures while separating text normalization, audio output and downstream recognition. |
| [vim](skills/vim/SKILL.md) | Control startup/modelines and recover copied swap artifacts with understood completeness limits. |
| [wfuzz](skills/wfuzz/SKILL.md) | Compare HTTP hosts/parameters with baselines, response filters, bounded ID ranges and known session state. |
| [xxd](skills/xxd/SKILL.md) | Inspect exact byte ranges and reconstruct hex artifacts without silent patching or truncation mistakes. |
| [ysoserial](skills/ysoserial/SKILL.md) | Generate selected Java serialization fixtures without confusing producer failures, binary output and target effects. |

The 94 skills are documentation-reviewed but have not been executed or evaluated with an agent on Linux. See the [validation record](docs/validation.md). Source coverage, corrections and deferred candidates are recorded for [batch 1](docs/ctf-writeups-ingestion.md), [batch 2](docs/ctf-writeups-batch2.md), [batch 3](docs/ctf-writeups-batch3.md), [batch 4](docs/ctf-writeups-batch4.md), [batch 5](docs/ctf-writeups-batch5.md), [batch 6](docs/ctf-writeups-batch6.md) and [batch 7](docs/ctf-writeups-batch7.md).

## Simple structure

~~~text
skills/<tool>/
    SKILL.md                   # metadata and working instructions
    references/                # optional, only when useful
        sources.md             # optional source/maintenance notes

authoring/                     # schema, prompts and optional templates
docs/                          # harness setup and validation history
ingest/                        # local source documents, ignored by Git
evaluation/                    # optional test design and case template
scripts/                       # help capture and repository checker
tests/
profile/                       # optional shell settings
~~~

One `SKILL.md` is enough for a small skill. Use ordinary Markdown with the standard [Agent Skills frontmatter](https://agentskills.io/specification). Add references for substantial conditional detail, sources for useful maintenance evidence, or scripts for repeated executable logic. Required resources stay inside their own skill folder.

## Create or improve a skill

1. Choose a task or known mistake. Collect practical documentation, examples or transcripts using the [source guide](authoring/sources.md).
2. Use the [authoring prompt](authoring/create-skill.prompt.md) and [schema](authoring/schema.md). The [single template](authoring/skill.template.md) is optional. A short correction may be enough; skip tools with no useful guidance gap.
3. Review accuracy and remove repetition. The [review prompt](authoring/review-skill.prompt.md) and [evaluation guide](evaluation/README.md) support deeper checks when needed.
4. Add accepted skills to the catalogue above. Keep drafts/raw sources in ignored `work/` and test artifacts in `runs/`; retain useful portable findings in the skill or source notes.

Commands, interpretations and recovery advice need evidence. Documentation review, procedure execution and improved agent performance are different claims. Record only what was actually established.

## Repository checks

~~~bash
python3 scripts/check_repository.py
python3 -B -m unittest discover -s tests -v
~~~

These validate links, basic frontmatter, standalone packaging and helper behaviour. Linux tool execution and worker usefulness need separate checks. Compare successful outcomes, recovery and total task cost against a baseline.

`AGENTS.md` and `CLAUDE.md` are for authors maintaining this repository. Workers need selected skill folders only. Optional settings in `profile/` are separate from skill installation. Add a repository license when you choose distribution terms.
