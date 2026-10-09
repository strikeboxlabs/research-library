# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills add useful tool knowledge for agents that already use the CLI competently. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [7z](skills/7z/SKILL.md) | Inspect, test and extract archives; distinguish unsupported encryption from password or integrity failures. |
| [aureport](skills/aureport/SKILL.md) | Interpret existing TTY audit records and correlate events without misattributing copied logs. |
| [bash](skills/bash/SKILL.md) | Diagnose startup context, environment inheritance and redirection order in scripts/jobs. |
| [bloodhound-python](skills/bloodhound-python/SKILL.md) | Choose CE/legacy collectors, scope directory collection and diagnose authentication/import gaps. |
| [chisel](skills/chisel/SKILL.md) | Map normal/reverse forwards and SOCKS direction, explicit listeners and authenticated tunnel cleanup. |
| [consul](skills/consul/SKILL.md) | Inspect selected KV data, distinguish ACL permissions and validate configuration before reload decisions. |
| [curl](skills/curl/SKILL.md) | Preserve HTTP responses, hostname/TLS routing, literal paths and meaningful error evidence. |
| [dirsearch](skills/dirsearch/SKILL.md) | Discover scoped web paths; handle wordlist expansion, soft 404s, redirects and incomplete scans. |
| [evil-winrm](skills/evil-winrm/SKILL.md) | Establish WinRM sessions with known credentials and diagnose transport, access and transfer issues. |
| [exiftool](skills/exiftool/SKILL.md) | Read image/document metadata while preserving tag groups and treating identities as leads. |
| [ffuf](skills/ffuf/SKILL.md) | Compare paths/vhosts with bounded requests, measured baselines and understood filter combinations. |
| [ftp](skills/ftp/SKILL.md) | Retrieve selected binary files and diagnose passive/active data-channel failures. |
| [gdb](skills/gdb/SKILL.md) | Examine existing native core dumps with matching executables; interpret stacks, missing symbols and incomplete evidence. |
| [git](skills/git/SKILL.md) | Inspect historical file content and renames without changing the checkout. |
| [gobuster](skills/gobuster/SKILL.md) | Choose web discovery modes and interpret wildcard, redirect and access-control responses. |
| [gpp-decrypt](skills/gpp-decrypt/SKILL.md) | Decode captured GPP cpassword values; distinguish the Ruby and Python implementations. |
| [hashcat](skills/hashcat/SKILL.md) | Check NT/Kerberos/APR1 records or binary Password Safe v3 files with correct mode and result handling. |
| [impacket-getnpusers](skills/impacket-getnpusers/SKILL.md) | Check selected accounts for AS-REP material without password guessing. |
| [impacket-gettgt](skills/impacket-gettgt/SKILL.md) | Obtain and select a Kerberos file cache using known credentials. |
| [impacket-getuserspns](skills/impacket-getuserspns/SKILL.md) | Separate SPN enumeration from selected service-ticket requests for an offline audit. |
| [impacket-reg](skills/impacket-reg/SKILL.md) | Query selected remote registry keys while accounting for hive context and service-state changes. |
| [impacket-rpcmap](skills/impacket-rpcmap/SKILL.md) | Distinguish scoped RPC interface binding, automatic fallback probes and actual method calls. |
| [impacket-secretsdump](skills/impacket-secretsdump/SKILL.md) | Parse SAM/SYSTEM or offline NTDS snapshots, or perform a selected-account replication audit. |
| [impacket-smbserver](skills/impacket-smbserver/SKILL.md) | Run a temporary bound SMB transfer share with explicit authentication and verified file transfer. |
| [jdb](skills/jdb/SKILL.md) | Attach to a JVM, reach relevant breakpoints and inspect suspended frames with understood evaluation effects. |
| [john](skills/john/SKILL.md) | Run bounded Jumbo checks on NT/NetNTLMv2/AS-REP and converted ZIP artifacts. |
| [kerbrute](skills/kerbrute/SKILL.md) | Check a bounded candidate username list against a selected KDC and interpret incomplete results. |
| [kinit](skills/kinit/SKILL.md) | Obtain MIT Kerberos tickets in an explicit cache, including existing-certificate PKINIT. |
| [ldapsearch](skills/ldapsearch/SKILL.md) | Query AD using simple bind or Kerberos, correct bases/filters and paged results. |
| [mdbtools](skills/mdbtools/SKILL.md) | Inventory and export selected Access database tables without corrupting field interpretation. |
| [mysql](skills/mysql/SKILL.md) | Diagnose socket/TCP and account identity, inspect metadata and understand LOCAL file access. |
| [ncat](skills/ncat/SKILL.md) | Interact with simple TCP services and distinguish line endings, EOF and connection/idle timeouts. |
| [netexec](skills/netexec/SKILL.md) | Validate known SMB credentials while controlling pair combinations and interpreting partial results. |
| [nmap](skills/nmap/SKILL.md) | Keep TCP/UDP and IPv4/IPv6 coverage explicit; interpret service probes and uncertain states. |
| [openssl](skills/openssl/SKILL.md) | Inspect requests/certificates, convert DER/PEM and distinguish signatures, issued identity and trust. |
| [proxychains](skills/proxychains/SKILL.md) | Route compatible TCP clients with a task-specific config and verify DNS/transport limitations. |
| [pspy](skills/pspy/SKILL.md) | Observe short-lived commands and scheduled jobs while accounting for missing process evidence. |
| [python-http-server](skills/python-http-server/SKILL.md) | Serve a dedicated directory temporarily and interpret transfer/callback evidence. |
| [readpst](skills/readpst/SKILL.md) | Convert PST email into searchable messages while preserving context and conversion limits. |
| [script](skills/script/SKILL.md) | Allocate a util-linux PTY or capture a terminal session with correct exit/logging semantics. |
| [searchsploit](skills/searchsploit/SKILL.md) | Search and inspect local exploit candidates without confusing title matches with applicability. |
| [smbclient](skills/smbclient/SKILL.md) | List shares and retrieve selected files with Samba; distinguish listing, read access and authentication. |
| [snmpwalk](skills/snmpwalk/SKILL.md) | Query bounded SNMP subtrees/instances and distinguish timeout, coverage and BITS rendering. |
| [ss](skills/ss/SKILL.md) | Inspect actual listeners/connections, address families, process visibility and namespaces. |
| [ssh](skills/ssh/SKILL.md) | Forward a remote loopback service and diagnose bind, destination and application-hostname failures. |
| [strace](skills/strace/SKILL.md) | Trace actual file/network operations and interpret config lookups and failed calls. |
| [strings](skills/strings/SKILL.md) | Extract binary text with file offsets and alternate encodings for evidence-led triage. |
| [sudo](skills/sudo/SKILL.md) | Interpret RunAs policy, environment handling and sudoedit copy-back behaviour. |
| [tcpdump](skills/tcpdump/SKILL.md) | Capture scoped traffic and distinguish packet evidence from application-level conclusions. |
| [text2wave](skills/text2wave/SKILL.md) | Generate speech fixtures while separating text normalization, audio output and downstream recognition. |
| [wfuzz](skills/wfuzz/SKILL.md) | Compare HTTP hosts/parameters with controlled baselines, payload pairing and session state. |

The 51 skills are documentation-reviewed but have not been executed or evaluated with an agent on Linux. See the [validation record](docs/validation.md). The CTF ingestion records explain [the first 16 additions](docs/ctf-writeups-ingestion.md), [the second batch's 13 additions and five enrichments](docs/ctf-writeups-batch2.md), and [the third batch's 21 additions and 10 enrichments](docs/ctf-writeups-batch3.md), including source corrections and deferred candidates.

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
