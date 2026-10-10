# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills supply tool selection and on-demand operational knowledge for capable CLI agents on the Linux distribution/image we deploy and control. A later pass on that image will add verified binary paths and relevant environment facts to the references. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [7z](skills/7z/SKILL.md) | Inspect/extract archives and disk images; diagnose backup format, listfile, wildcard and symlink boundaries. |
| [adb](skills/adb/SKILL.md) | Inspect a selected Android device and separate reverse routing, transfer privileges, proxy settings and CA trust. |
| [ansible-vault](skills/ansible-vault/SKILL.md) | Extract and decrypt vault objects without loading playbooks or confusing vault passwords with plaintext values. |
| [apktool](skills/apktool/SKILL.md) | Decode APK resources, resolve framework gaps and distinguish a rebuild from valid Android signing. |
| [aureport](skills/aureport/SKILL.md) | Interpret existing TTY audit records and correlate events without misattributing copied logs. |
| [awk](skills/awk/SKILL.md) | Separate program source, literal data and regexes; recognize quoted CSV and binary-transfer limits. |
| [aws](skills/aws/SKILL.md) | Inspect explicit S3/DynamoDB endpoints, bound reads and interpret pagination, object keys and composite keys. |
| [backy](skills/backy/SKILL.md) | Run an archive-only JSON task and distinguish skipped cycles, destructive sync options and verified backup output. |
| [base64](skills/base64/SKILL.md) | Preserve transferred bytes and distinguish digest bytes, base64url and HTTP form-encoding layers. |
| [bash](skills/bash/SKILL.md) | Diagnose startup, restricted sessions, pattern comparisons, data reparsing, environment inheritance, filename expansion and redirection order. |
| [bbot](skills/bbot/SKILL.md) | Select reconnaissance presets/modules, retain scan evidence and diagnose custom-module or privileged loader behavior. |
| [bloodhound-python](skills/bloodhound-python/SKILL.md) | Collect scoped AD directory evidence with BloodHound.py from Linux. Use when selecting CE versus legacy collectors, diagnosing Kerberos/DNS failures or distinguishing collected rights from current access. |
| [bloodyad](skills/bloodyad/SKILL.md) | Selected AD object reads, membership/owner changes and read-back with bloodyAD. |
| [bmap](skills/bmap/SKILL.md) | Inspect trailing filesystem slack with the legacy reader while preserving allocation and qualifying recovery evidence. |
| [bzip2](skills/bzip2/SKILL.md) | Recover one verified compression layer, preserving source bytes and partial/naming distinctions. |
| [cargo](skills/cargo/SKILL.md) | Existing Rust CLI builds/runs, selected target/profile and dependency-resolution limits. |
| [cast](skills/cast/SKILL.md) | Read Ethereum blocks, transactions and contract getters; distinguish ABI/state evidence from published transactions. |
| [certipy](skills/certipy/SKILL.md) | Enumerate AD CS configuration, request selected certificates, authenticate with a PFX, recover through a permitted key-credential write and update selected UPNs from Linux. Use to connect template/CA findings to enrollment prerequisites, issuance results and current certificate-mapping behavior. |
| [cewl](skills/cewl/SKILL.md) | Collect scoped website vocabulary with deliberate depth, filtering and plain-word output for offline audits. |
| [chisel](skills/chisel/SKILL.md) | Build and diagnose explicit Chisel port forwards or reverse SOCKS connections. Use when client/server direction, listener exposure, endpoint reachability or fingerprint authentication is unclear. |
| [composer](skills/composer/SKILL.md) | PHP dependency/lock inspection, selected installs and project-script execution context. |
| [consul](skills/consul/SKILL.md) | Inspect selected KV data, distinguish ACL permissions and validate configuration before reload decisions. |
| [cp](skills/cp/SKILL.md) | Copy selected directories and diagnose path, permission and metadata-preservation differences. |
| [credentialmanager](skills/credentialmanager/SKILL.md) | Read a selected stored Windows credential through the installed CredentialManager PowerShell module in a remote session. Use from a Linux worker when network-logon or SYSTEM context differs from the intended user credential set. |
| [cryptsetup](skills/cryptsetup/SKILL.md) | Inspect and unlock LUKS image copies with read-only mappings and filesystem-aware mounting. |
| [curl](skills/curl/SKILL.md) | Capture HTTP/API evidence, Rails report boundaries, helpdesk email/signup trust and Grafana file reads while preserving routing, bytes and application-result distinctions. |
| [dd](skills/dd/SKILL.md) | Extract measured image byte ranges without hardcoded header sizes, overwrite or unnoticed short copies. |
| [derby-ij](skills/derby-ij/SKILL.md) | Inspect consistent Derby copies with embedded JDBC, schema discovery, bounded SQL and understood display/lock limits. |
| [diff](skills/diff/SKILL.md) | Compare acquired trees against a matching baseline and distinguish content changes from incomplete comparisons. |
| [dig](skills/dig/SKILL.md) | Query explicit DNS servers and compare authoritative, cached, negative and application resolver views. |
| [dirsearch](skills/dirsearch/SKILL.md) | Discover scoped web paths; narrow partial-name candidates and handle expansion, soft 404s and redirects. |
| [dive](skills/dive/SKILL.md) | Inspect local image layers, distinguish deletion markers and recover selected historical file bytes. |
| [dnstool](skills/dnstool/SKILL.md) | Query, add and remove a selected AD-integrated DNS A record with krbrelayx dnstool from Linux. Use to distinguish LDAP bind, DNS-node permissions, stored changes and actual DNS resolution. |
| [docker](skills/docker/SKILL.md) | Pinned tool environments, selected container exec/device access, mount attribution, registry/source inspection and image/archive transfer. |
| [docker-compose](skills/docker-compose/SKILL.md) | Resolve/run an explicit project and diagnose capability grants, privileged wrappers and cleanup effects. |
| [dotnet](skills/dotnet/SKILL.md) | Distinguish .NET Framework/platform targets, select SDK/runtime context and build or run reviewed projects explicitly. |
| [dpkg-deb](skills/dpkg-deb/SKILL.md) | Build/inspect Debian archives and retain control-hook, ownership and privileged-installer boundaries. |
| [dpkg-query](skills/dpkg-query/SKILL.md) | Match file ownership, installed state and complete Debian/Ubuntu package versions to the applicable vendor advisory. |
| [ebook-convert](skills/ebook-convert/SKILL.md) | Convert e-books with explicit formats and diagnose resource inclusion and transformation stages. |
| [evil-winrm](skills/evil-winrm/SKILL.md) | Open a Windows WinRM session from Linux with Evil-WinRM using known credentials. Use for transport/authentication diagnosis, current token inspection, selected file transfers and distinguishing WinRM access from SMB login success. |
| [exiftool](skills/exiftool/SKILL.md) | Read image/document metadata while preserving tag groups and treating identities as leads. |
| [fail2ban-client](skills/fail2ban-client/SKILL.md) | Trace failures through jails, filters and actions; diagnose bans and perform selected unban/reload operations. |
| [fakedns](skills/fakedns/SKILL.md) | Serve scoped synthetic DNS answers and reproduce query-count rebinding with resolver/cache evidence. |
| [feroxbuster](skills/feroxbuster/SKILL.md) | Bound web discovery and interpret wildcard filters, parent-directory denial, accessible children and incomplete scans. |
| [ffuf](skills/ffuf/SKILL.md) | Compare paths/vhosts with bounded framework candidates, method context, controls and understood filters. |
| [fickling](skills/fickling/SKILL.md) | Inspect pickle streams statically and distinguish findings, scanner failures and incomplete model coverage. |
| [file](skills/file/SKILL.md) | Classify artifacts without confusing format labels, managed assemblies, transfer integrity and runtime compatibility. |
| [find](skills/find/SKILL.md) | Scope searches and timestamp inventories while interpreting permissions, emptiness, traversal errors and action boundaries. |
| [findmnt](skills/findmnt/SKILL.md) | Identify covering filesystems and exact mountpoints while preserving namespace and host-source uncertainty. |
| [firefox-decrypt](skills/firefox-decrypt/SKILL.md) | Recover saved logins from one authorized offline Mozilla profile; diagnose key/NSS compatibility and incomplete records. |
| [forge](skills/forge/SKILL.md) | Diagnose Foundry builds with explicit project/compiler context and correctly interpreted helper trace logs. |
| [ftp](skills/ftp/SKILL.md) | Transfer selected files, diagnose data channels and verify an authorised upload-to-web mapping without inferring code execution. |
| [gcc](skills/gcc/SKILL.md) | Compile selected C tools/shared libraries; distinguish build stages, ABI, declarations and runtime compatibility. |
| [gdb](skills/gdb/SKILL.md) | Follow native core frames/state to a bounded diagnosis, or inspect a controlled live reproduction. |
| [gdbserver](skills/gdbserver/SKILL.md) | Debug controlled remote programs over SSH with understood transport, connection modes and process lifetime. |
| [getcap](skills/getcap/SKILL.md) | Verify file capabilities and distinguish stored flags, execution conditions and current process authority. |
| [getent](skills/getent/SKILL.md) | Resolve NSS users/groups and distinguish directory membership from current process privileges. |
| [getfacl](skills/getfacl/SKILL.md) | Explain POSIX ACL masks, named identities, parent traversal and default inheritance for access failures. |
| [ghidra](skills/ghidra/SKILL.md) | Export selected native-function decompilations headlessly and trace file/database logic without inferring runtime success. |
| [git](skills/git/SKILL.md) | Inspect history, stored links/submodules and remote URLs; check scoped patches and diagnose local hooks. |
| [git-dumper](skills/git-dumper/SKILL.md) | Recover exposed Git data within an isolated environment and distinguish missing objects, checkout failures and incomplete history. |
| [go](skills/go/SKILL.md) | Build reviewed CLI projects; resolve generated imports and distinguish command construction, execution and unchecked results. |
| [gobuster](skills/gobuster/SKILL.md) | Choose web discovery modes and interpret wildcard, redirect, method and validation responses. |
| [gpg](skills/gpg/SKILL.md) | Decrypt a selected OpenPGP backup with GnuPG using its known passphrase or matching secret key. Use to distinguish symmetric encryption, key material, pinentry behavior and partial plaintext from a valid recovery. |
| [gpp-decrypt](skills/gpp-decrypt/SKILL.md) | Decode captured GPP cpassword values; distinguish the Ruby and Python implementations. |
| [grafana2hashcat](skills/grafana2hashcat/SKILL.md) | Convert verified historical Grafana records with iamaldi’s installed converter; preserve literal salts, cost, row mapping and full-verifier interpretation. |
| [grep](skills/grep/SKILL.md) | Filter literal or regex text while preserving alternative/combined conditions, binary handling and error evidence. |
| [groups](skills/groups/SKILL.md) | Inspect the current Linux process group names or a selected account lookup with GNU groups. Use to distinguish live session membership from directory membership and application authorization. |
| [gzip](skills/gzip/SKILL.md) | Recover selected gzip streams; interpret suffixes, concatenation and failed integrity checks. |
| [h2csmuggler](skills/h2csmuggler/SKILL.md) | Distinguish h2c upgrade acceptance, tunneled application replies and actual access-control differences. |
| [hashcat](skills/hashcat/SKILL.md) | Pattern/rule candidate generation and bounded offline record checks; format conversion, full-verifier confirmation and incomplete-run interpretation. |
| [hashid](skills/hashid/SKILL.md) | Identify candidate hash formats offline and handle ambiguous matches, unsupported prefixes and format hints. |
| [hostname](skills/hostname/SKILL.md) | Identify configured namespace-local addresses and distinguish DNS, address order and reachability. |
| [httpie](skills/httpie/SKILL.md) | Construct JSON API requests offline and interpret selected lookups with explicit input and status handling. |
| [hydra](skills/hydra/SKILL.md) | Perform scoped protocol/form authentication tests with bounded attempts and verified response classification. |
| [iconv](skills/iconv/SKILL.md) | Convert captured text with explicit encodings; distinguish UTF-16 byte order, terminators and lossy recovery. |
| [id](skills/id/SKILL.md) | Verify real/effective user/group IDs in the current context and distinguish named-account lookup from execution privilege. |
| [ifconfig](skills/ifconfig/SKILL.md) | Inspect Linux net-tools interface addresses, netmasks and link counters with ifconfig. Use when an internal execution vantage differs from an external address and subnet or route assumptions need correction. |
| [iis-shortname-scanner](skills/iis-shortname-scanner/SKILL.md) | Check IIS short-name disclosure and distinguish partial aliases, response ambiguity and confirmed full paths. |
| [ike-scan](skills/ike-scan/SKILL.md) | Interpret an IKE endpoint's initial proposal response, notify errors and vendor fingerprints without claiming authentication. |
| [ilspycmd](skills/ilspycmd/SKILL.md) | Inspect .NET types, time-seeded crypto, serialization and archive-write paths without launching the assembly. |
| [impacket-addcomputer](skills/impacket-addcomputer/SKILL.md) | Selected AD computer-account creation, method differences and owned cleanup. |
| [impacket-dacledit](skills/impacket-dacledit/SKILL.md) | Inspect/back up DACLs, apply precise delegation and verify ACE removal or restoration without losing concurrent state. |
| [impacket-getadusers](skills/impacket-getadusers/SKILL.md) | Query selected AD user metadata and interpret filtering, email requirements and DC-local logon dates. |
| [impacket-getnpusers](skills/impacket-getnpusers/SKILL.md) | Check selected accounts for AS-REP material without password guessing. |
| [impacket-getst](skills/impacket-getst/SKILL.md) | Request selected Kerberos service tickets and interpret SPNs, existing delegation and saved cache identity. |
| [impacket-gettgt](skills/impacket-gettgt/SKILL.md) | Obtain a Kerberos file credential cache using known credentials with Impacket getTGT. Use when Linux LDAP or SMB clients need a ticket and cache identity, hostname or clock errors interrupt authentication. |
| [impacket-getuserspns](skills/impacket-getuserspns/SKILL.md) | Separate SPN enumeration from selected service-ticket requests for an offline audit. |
| [impacket-lookupsid](skills/impacket-lookupsid/SKILL.md) | Resolve bounded RID ranges while preserving SID scope, principal types and incomplete-lookup evidence. |
| [impacket-mssqlclient](skills/impacket-mssqlclient/SKILL.md) | Inspect SQL Server authentication, cache/SPN selection, SQL identity and command-execution configuration. |
| [impacket-ntlmrelayx](skills/impacket-ntlmrelayx/SKILL.md) | Configure a selected NTLM relay with Impacket and distinguish inbound authentication, target authentication and the chosen protocol action. Use for controlled relay testing with explicit listeners, destinations and result evidence. |
| [impacket-owneredit](skills/impacket-owneredit/SKILL.md) | Exact AD owner SID read/write and restoration constraints. |
| [impacket-psexec](skills/impacket-psexec/SKILL.md) | Execute selected Windows commands through Impacket services and distinguish authentication, execution and cleanup. |
| [impacket-reg](skills/impacket-reg/SKILL.md) | Query selected remote registry keys while accounting for hive context and service-state changes. |
| [impacket-rpcmap](skills/impacket-rpcmap/SKILL.md) | Distinguish scoped RPC interface binding, automatic fallback probes and actual method calls. |
| [impacket-secretsdump](skills/impacket-secretsdump/SKILL.md) | Parse existing Windows SAM/SYSTEM, SECURITY or NTDS snapshots, perform approved remote member-host acquisition or a selected-account AD replication audit with Impacket secretsdump. Use to distinguish offline evidence, current credentials and incomplete results. |
| [impacket-smbclient](skills/impacket-smbclient/SKILL.md) | Impacket SMB share/file operations with independent authentication and transfer guidance. |
| [impacket-smbexec](skills/impacket-smbexec/SKILL.md) | Run selected Windows commands through the Service Control Manager with Impacket smbexec from Linux. Use when SMB administrative access exists and service execution, output shares or SYSTEM versus user context matters. |
| [impacket-smbserver](skills/impacket-smbserver/SKILL.md) | Run a temporary bound SMB transfer share with explicit authentication and verified file transfer. |
| [impacket-ticketer](skills/impacket-ticketer/SKILL.md) | Generate and inspect selected Kerberos service tickets with known service keys with Impacket ticketer. Use to distinguish service keys, SPNs, identity fields, cache creation and actual service acceptance in an authorized lab. |
| [impacket-wmiexec](skills/impacket-wmiexec/SKILL.md) | WMI/DCOM command execution, SMB output stages and cleanup interpretation. |
| [inveigh](skills/inveigh/SKILL.md) | Capture a bounded selected HTTP NTLM authentication exchange with cross-platform Inveigh. Use when an application sends outbound integrated authentication and identity, listener exposure or challenge-response interpretation needs evidence. |
| [ip](skills/ip/SKILL.md) | Explain Linux route selection using local addresses, policy rules, prefix specificity and namespace-aware lookups. |
| [ipcs](skills/ipcs/SKILL.md) | Inspect System V shared-memory metadata, keys, segment IDs, permissions and namespace limits. |
| [ipfs](skills/ipfs/SKILL.md) | Inspect local Kubo blocks, resolve UnixFS roots and recover selected files without fetching from peers. |
| [ipset](skills/ipset/SKILL.md) | Inspect kernel set types/members and compare ban exports with actual membership and firewall policy. |
| [iptables](skills/iptables/SKILL.md) | Inspect firewall backend, family and packet path with ordered rules, state, source/destination ports and saved-versus-live limits. |
| [iptables-save](skills/iptables-save/SKILL.md) | Capture ruleset evidence while distinguishing output-file effects, coverage, restore and persistence. |
| [jadx](skills/jadx/SKILL.md) | Inspect APK resources and DEX call paths while recovering from incomplete decompilation. |
| [jarsigner](skills/jarsigner/SKILL.md) | Interpret JAR signature coverage, unsigned zero exits, strict warnings and Android verifier boundaries. |
| [java](skills/java/SKILL.md) | Launch a selected Java CLI with explicit runtime/classpath and distinguish missing classes from application failure. |
| [javac](skills/javac/SKILL.md) | Compile reviewed Java sources into a controlled output tree and diagnose release/API/processor differences. |
| [jdb](skills/jdb/SKILL.md) | Attach to a JVM, reach relevant breakpoints and inspect suspended frames with understood evaluation effects. |
| [jenkins-cli](skills/jenkins-cli/SKILL.md) | Verify controller identity/permissions and inspect an existing build log; distinguish transports, local authentication files and historical disclosure evidence. |
| [jenkins-offline-decrypt](skills/jenkins-offline-decrypt/SKILL.md) | Matched-backup Jenkins Secret recovery and implementation/parser limits. |
| [john](skills/john/SKILL.md) | Run bounded offline checks with John the Ripper Jumbo on NT, NetNTLMv2, Kerberos, ZIP, KeePass, OpenPGP secret keys, bcrypt, phpass, raw MD5/SHA-256, sha512crypt or HS256 JWT artifacts. Use to choose formats, preserve records and interpret session results. |
| [jq](skills/jq/SKILL.md) | Preserve JSON types, select decoded account maps and construct requests/config transformations without corrupting evidence. |
| [jwt-tool](skills/jwt-tool/SKILL.md) | Inspect JWT fixtures and original-token HMAC matches; separate signing, claim mappings and application sessions. |
| [keepassxc-cli](skills/keepassxc-cli/SKILL.md) | Inspect a database with known unlock factors and retrieve exact entries/fields without broad disclosure. |
| [kerbrute](skills/kerbrute/SKILL.md) | Check a bounded candidate username list against a selected KDC and interpret incomplete results. |
| [kinit](skills/kinit/SKILL.md) | Obtain MIT Kerberos tickets in an explicit cache, including existing-certificate PKINIT. |
| [klist](skills/klist/SKILL.md) | Inspect a selected MIT Kerberos credential cache from Linux. Use to verify principal, realm, service and expiry before a client login, without confusing a cached ticket with application authorization. |
| [krbrelayx](skills/krbrelayx/SKILL.md) | Relay a selected Kerberos authentication exchange to an AD CS web endpoint with krbrelayx from Linux. Use when NTLM is unavailable and callback DNS naming, SPN selection, listener routing and certificate identity need explicit evidence. |
| [ldapsearch](skills/ldapsearch/SKILL.md) | Query AD or POSIX identities, groups, deleted objects and policy with explicit schema, authentication and coverage. |
| [ldbsearch](skills/ldbsearch/SKILL.md) | Inspect records in an offline SSSD LDB cache while preserving identity and attribute context. Use when strings output cannot map a value to an account or a cache query appears empty. |
| [ldconfig](skills/ldconfig/SKILL.md) | Inspect/refresh library caches and exercise a scoped writable-directory load with actual identity evidence. |
| [ldd](skills/ldd/SKILL.md) | Resolve trusted ELF dependencies and distinguish missing objects, unexpected paths and privileged-launch limits. |
| [less](skills/less/SKILL.md) | Inspect an existing Linux text artifact interactively with less while preserving literal content and search context. Use when wrapped configuration lines or embedded terminal controls obscure the evidence. |
| [lftp](skills/lftp/SKILL.md) | Use verified explicit FTPS for selected transfers and diagnose transport, data-channel and virtual-user access differences. |
| [linpeas](skills/linpeas/SKILL.md) | Scope enumeration checks and verify unfamiliar SUID helpers, execution conditions and vendor package evidence. |
| [logrotate](skills/logrotate/SKILL.md) | Preview actual rotation jobs and interpret state, skip conditions, permissions and hook identities. |
| [logrotten](skills/logrotten/SKILL.md) | Selected disposable-fixture logrotate race, path effects and write evidence. |
| [mail](skills/mail/SKILL.md) | Distinguish GNU Mailutils and S-nail flags, subject handling, attachments and submission evidence. |
| [make](skills/make/SKILL.md) | Build reviewed existing tool targets; diagnose configured features, compiler failures and stale artifacts without implying installation. |
| [marshalsec](skills/marshalsec/SKILL.md) | Select unmarshalling fixtures and distinguish local test execution, JNDI stages and runtime dependencies. |
| [masscan](skills/masscan/SKILL.md) | Discover scoped TCP listeners with explicit configuration and host/protocol-preserving service follow-up. |
| [md5sum](skills/md5sum/SKILL.md) | Reproduce exact legacy checksum bytes and distinguish malformed, missing or mismatching manifests. |
| [mdbtools](skills/mdbtools/SKILL.md) | Inventory and export selected Access database tables without corrupting field interpretation. |
| [memcached-tool](skills/memcached-tool/SKILL.md) | Inspect cache/slab statistics and bounded key/value exports with the existing protocol-aware helper. |
| [minecraft-console-client](skills/minecraft-console-client/SKILL.md) | Use a headless Minecraft Java session and distinguish protocol support, offline identity, client commands and server responses. |
| [mount](skills/mount/SKILL.md) | Mount an identified block filesystem for selected reads or authorized changes; distinguish namespace/source identity, journal writes and busy cleanup. |
| [mount-cifs](skills/mount-cifs/SKILL.md) | Mount SMB shares read-only; distinguish metadata timestamps, dialects, signing and local/server permissions. |
| [mount-nfs](skills/mount-nfs/SKILL.md) | Mount selected NFS exports read-only; diagnose version, identity, locking and mount-state evidence. |
| [msf-pattern](skills/msf-pattern/SKILL.md) | Pair Metasploit pattern generation and offset lookup without confusing heuristic matches or overwritten fields. |
| [msfconsole](skills/msfconsole/SKILL.md) | Select and configure Framework modules; manage matching handlers, jobs and sessions with explicit outcome checks. |
| [msfvenom](skills/msfvenom/SKILL.md) | Generate selected payload artifacts with matching platform, architecture, format and handler requirements. |
| [mysql](skills/mysql/SKILL.md) | Explicit connection/account context, selected Mattermost records, string semantics and native/client/server execution boundaries. |
| [mysqldump](skills/mysqldump/SKILL.md) | Back up a selected database and distinguish SQL failures, compression integrity, object coverage and validated recovery. |
| [nc](skills/nc/SKILL.md) | TCP connections/listeners, EOF and variant differences, with authorized traditional-netcat executable streams. |
| [ncat](skills/ncat/SKILL.md) | Interact with TCP protocols, capture selected callbacks and interpret Memcached values with correct framing and timeouts. |
| [neo4j-admin](skills/neo4j-admin/SKILL.md) | Set the native database password before first startup; distinguish setup history from current database/OS credentials. |
| [netexec](skills/netexec/SKILL.md) | Validate known SMB credentials, interpret share checks, read selected user metadata and inspect LDAP protection, AD CS endpoints and machine-account quota with NetExec on selected lab hosts. Use to avoid unintended credential combinations and distinguish authentication, password status, privilege indicators and path permissions. |
| [nginx](skills/nginx/SKILL.md) | Inspect selected configuration, worker/file authority, WebDAV conditions and validation-versus-live-state evidence. |
| [nimble](skills/nimble/SKILL.md) | Nim dependency inspection, selected provisioning and build-context diagnosis. |
| [nmap](skills/nmap/SKILL.md) | Keep protocol, address and IPsec vantage explicit; interpret service probes and uncertain states. |
| [node](skills/node/SKILL.md) | Resolve CommonJS dependencies, reproduce selected module precedence and receive a bounded Socket.IO event. |
| [npbackup-cli](skills/npbackup-cli/SKILL.md) | Select exact backup snapshots, recover a file and distinguish backend writes from wrapper policy/status failures. |
| [oathtool](skills/oathtool/SKILL.md) | Generate known-secret TOTP and diagnose encoding, parameter and clock mismatches. |
| [objdump](skills/objdump/SKILL.md) | Inspect headers, imported calls and bounded disassembly while separating bytes, source lines and runtime evidence. |
| [omv-rpc](skills/omv-rpc/SKILL.md) | OpenMediaVault mounted-filesystem queries, local RPC privilege boundaries and selected installation/job output. |
| [openssl](skills/openssl/SKILL.md) | Inspect certificates, key formats and TLS mail/FTP sessions; recover known-format AES-CBC artifacts with explicit byte/padding interpretation. |
| [openvpn](skills/openvpn/SKILL.md) | Use reviewed client profiles; distinguish tunnel initialization, selected routes, DNS and service reachability. |
| [pacman](skills/pacman/SKILL.md) | Inspect Arch package metadata, payloads, scriptlets and ownership before choosing an installation transaction. |
| [passthecert](skills/passthecert/SKILL.md) | Python certificate LDAP authentication and selected RBCD change/read-back/removal. |
| [pd4cmd](skills/pd4cmd/SKILL.md) | Convert reviewed HTML with PD4ML; diagnose entrypoints, resource access, layout and stale PDF output. |
| [peda](skills/peda/SKILL.md) | Load the installed GDB extension explicitly and correlate x86 registers, code, stack and call arguments. |
| [phantomjs](skills/phantomjs/SKILL.md) | Legacy CLI rendering, document capture and load/result interpretation. |
| [php](skills/php/SKILL.md) | Serve a reviewed local web test and inspect PHP configuration, extensions, PHARs, encoding and upload validation. |
| [phpggc](skills/phpggc/SKILL.md) | Select serialization chains by dependency and trigger; preserve bytes and validate the actual parser/object lifecycle. |
| [pip](skills/pip/SKILL.md) | Compare manifest and installed versions; match interpreter/wheel compatibility and control dependency/build fallback. |
| [printerbug](skills/printerbug/SKILL.md) | Trigger one authorized Windows spooler RPC authentication callback with krbrelayx printerbug from Linux. Use to distinguish RPC bind, notification errors and independently observed NTLM or Kerberos backconnects. |
| [procyon](skills/procyon/SKILL.md) | Recover Java methods from local JAR/class files and trace plugin settings while qualifying reconstruction and runtime evidence. |
| [proxychains](skills/proxychains/SKILL.md) | Route compatible Linux TCP clients through an explicit ProxyChains-NG configuration. Use when SOCKS or HTTP CONNECT policy, DNS behavior or unsupported raw/UDP traffic causes misleading failures. |
| [ps](skills/ps/SKILL.md) | Inspect process identity/state and targeted procfs evidence without confusing NUL-separated or mutable metadata. |
| [ps2pdf](skills/ps2pdf/SKILL.md) | Convert reviewed PostScript and diagnose status, template errors and Ghostscript file-access controls. |
| [pspy](skills/pspy/SKILL.md) | Correlate short-lived processes with jobs/actions while retaining exact paths, identities and visibility limits. |
| [psql](skills/psql/SKILL.md) | Connect to a known PostgreSQL database, inspect schema, export bounded results and administer selected server files/WAL archiving with psql. Use when socket versus TCP authentication, SQL role, startup files, quoting or partial output obscures a result. |
| [pwntools](skills/pwntools/SKILL.md) | Complete framed exchanges, interpret timeouts/EOF and reconstruct integer fields with explicit widths and byte order. |
| [pygpoabuse](skills/pygpoabuse/SKILL.md) | Plan isolated lab GPO task tests with explicit commands, client scope, before-state and incomplete-cleanup handling. |
| [pypykatz](skills/pypykatz/SKILL.md) | Inspect LSASS snapshots and derive known-password NT values while preserving identity and artifact type. |
| [python-http-server](skills/python-http-server/SKILL.md) | Serve selected local files or receive a bounded controlled POST callback with Python's http.server. Use when bind addresses, directory exposure, transfer verification or callback logs need interpretation. |
| [python3](skills/python3/SKILL.md) | Inspect source, output and bytes; decode SAML, query with existing PyMySQL or diagnose stateful WebSocket messages. |
| [rdate](skills/rdate/SKILL.md) | Diagnose clock skew with print-only SNTP queries and distinguish protocol, timezone and synchronization issues. |
| [readelf](skills/readelf/SKILL.md) | Map ELF layouts and inspect dynamic dependencies/symbols while separating artifact metadata from runtime behavior. |
| [readpst](skills/readpst/SKILL.md) | Convert PST/supported OST mail while accounting for MIME, image attachments and conversion limits. |
| [redis-cli](skills/redis-cli/SKILL.md) | Inspect selected Redis values with known authentication, explicit databases and bounded cursor scans. |
| [responder](skills/responder/SKILL.md) | Separate name observation from active authentication listeners and preserve complete capture evidence. |
| [restic](skills/restic/SKILL.md) | Select backup snapshots/paths and restore into a new directory with understood helpers, filters and locks. |
| [rlwrap](skills/rlwrap/SKILL.md) | Local Readline editing for a selected client, with history and remote-terminal limits. |
| [ropgadget](skills/ropgadget/SKILL.md) | Inspect gadget candidates with understood search depth, address filters and complete instruction effects. |
| [rpcclient](skills/rpcclient/SKILL.md) | Resolve RPC identities and perform selected SAMR account changes with distinct rights and outcome evidence. |
| [rsh](skills/rsh/SKILL.md) | GNU rsh command execution, rlogin fallback and legacy trust interpretation. |
| [rsync](skills/rsync/SKILL.md) | Inspect daemon modules and retrieve a selected file with explicit transport, destination and partial-copy handling. |
| [rustbuster](skills/rustbuster/SKILL.md) | Choose path, DNS, virtual-host or request-marker discovery with meaningful controls and filters. |
| [rustscan](skills/rustscan/SKILL.md) | Discover scoped TCP ports, tune resource/timeout behavior and hand findings to Nmap with separate evidence. |
| [samdump2](skills/samdump2/SKILL.md) | Extract matching legacy SAM/SYSTEM records and detect unsupported formats or misleading empty-password values. |
| [scp](skills/scp/SKILL.md) | Transfer selected files and recover from authentication, SFTP-subsystem, path or partial-copy failures. |
| [screen](skills/screen/SKILL.md) | Identify and resume sessions with understood sharing, ownership, terminal and multiuser requirements. |
| [script](skills/script/SKILL.md) | Allocate a util-linux PTY or capture a terminal session with correct exit/logging semantics. |
| [searchor](skills/searchor/SKILL.md) | Generate engine-specific search URLs and account for local history, browser and clipboard effects. |
| [searchsploit](skills/searchsploit/SKILL.md) | Search and inspect local exploit candidates without confusing title matches with applicability. |
| [sendmail](skills/sendmail/SKILL.md) | Submit requested messages with explicit envelope recipients and distinguish queue acceptance from delivery. |
| [sharp-gpoabuse](skills/sharp-gpoabuse/SKILL.md) | Apply a selected GPO local-administrator change with SharpGPOAbuse through a remote Windows command session. Use from Linux to distinguish policy write rights, linked client scope, application and fresh token evidence. |
| [shocker](skills/shocker/SKILL.md) | Match a reviewed file-handle test build and qualify selected-file recovery and isolation prerequisites. |
| [showmount](skills/showmount/SKILL.md) | Inspect NFS export advertisements while distinguishing MOUNT-service limits, NFSv4 and actual access. |
| [smbclient](skills/smbclient/SKILL.md) | Retrieve selected SMB files with explicit identity and distinguish share labels, file permissions and execution evidence. |
| [smbmap](skills/smbmap/SKILL.md) | Inventory SMB access without default write probes and control traversal and selected downloads. |
| [smbpasswd](skills/smbpasswd/SKILL.md) | Change a known account's remote SMB password while distinguishing required changes, resets and local database operations. |
| [smtp-user-enum](skills/smtp-user-enum/SKILL.md) | Compare scoped SMTP recipient responses without treating tool classifications as mailbox proof. |
| [snap](skills/snap/SKILL.md) | Inspect revisions, confinement and change tasks; distinguish signature checks from executable install hooks. |
| [snmpwalk](skills/snmpwalk/SKILL.md) | Query bounded OIDs, distinguish contact text from credentials and load hardware inventory guidance on demand. |
| [sqlite3](skills/sqlite3/SKILL.md) | Inspect coherent SQLite copies and export selected Grafana verifier rows without confusing storage metadata, salt bytes or account mapping. |
| [sqlmap](skills/sqlmap/SKILL.md) | Test a selected HTTP parameter and inspect scoped database metadata or samples with request/session fidelity. |
| [ss](skills/ss/SKILL.md) | Inspect actual listeners/connections, address families, process visibility and namespaces. |
| [ssh](skills/ssh/SKILL.md) | Selected account/key login, authorized public-key file changes, GSSAPI identity and loopback forwarding with explicit result/cleanup. |
| [ssh-keygen](skills/ssh-keygen/SKILL.md) | Derive public keys and compare fingerprints while preserving private artifacts and format distinctions. |
| [ssh-username-enum](skills/ssh-username-enum/SKILL.md) | Selected OpenSSH malformed-authentication account oracle with legacy-helper compatibility and control/result limits. |
| [stoken](skills/stoken/SKILL.md) | Import selected SecurID software tokens, generate codes and diagnose state/PIN/time differences. |
| [strace](skills/strace/SKILL.md) | Trace file/network failures and interpret acquired reads with process, descriptor, byte-count and tracing-side-effect context. |
| [strings](skills/strings/SKILL.md) | Triage binary files with GNU strings while retaining offsets and checking alternate encodings. Use when paths, error messages or UTF-16 text guide subsequent binary analysis. |
| [strongswan-ipsec](skills/strongswan-ipsec/SKILL.md) | Inspect existing VPN SAs and diagnose selector, transport-mode and application-path mismatches. |
| [stty](skills/stty/SKILL.md) | Inspect/save/restore terminal state and manage local relay echo/raw mode separately from a remote PTY. |
| [su](skills/su/SKILL.md) | Selected local account sessions with known credentials; login environment, PAM/terminal handling and effective-identity verification. |
| [sucrack](skills/sucrack/SKILL.md) | Bounded local su candidate checks; worker/rewrite choices, build features, prompt detection and independent account verification. |
| [sudo](skills/sudo/SKILL.md) | Interpret sudo policy, RunAs identities, helper paths, environment handling and sudoedit on Linux. Use when a permitted command behaves differently under sudo or a walkthrough overstates privilege from a policy listing. |
| [swaks](skills/swaks/SKILL.md) | Preview MIME and diagnose explicit SMTP stages, TLS verification and delivery evidence. |
| [systemctl](skills/systemctl/SKILL.md) | Diagnose selected systemd units and apply validated reload/restart changes with useful outcome checks. |
| [tail](skills/tail/SKILL.md) | Read bounded log suffixes and follow selected writers across rotation/truncation with evidence limits. |
| [tar](skills/tar/SKILL.md) | Extract selected members; diagnose mounted-content omissions, nested archives, ownership and partial/sidecar consistency. |
| [targetedkerberoast](skills/targetedkerberoast/SKILL.md) | Select existing-SPN or temporary-SPN ticket collection and verify directory state after write-enabled tests. |
| [tcpdump](skills/tcpdump/SKILL.md) | Capture scoped traffic at the correct interface/port, retain handshake evidence and distinguish application conclusions. |
| [text2wave](skills/text2wave/SKILL.md) | Generate speech fixtures while separating text normalization, audio output and downstream recognition. |
| [thrift](skills/thrift/SKILL.md) | Generate reviewed RPC bindings and distinguish compiler, transport, protocol and handler outcomes. |
| [tshark](skills/tshark/SKILL.md) | Correlate saved FTP/TLS/Kerberos traffic with conversation identity, pre-authentication fields and incomplete evidence. |
| [unbound-control](skills/unbound-control/SKILL.md) | Inspect resolver control/counters and change one live forwarding zone with verification and restoration. |
| [unzip](skills/unzip/SKILL.md) | Inspect ZIP names/CRCs and selected Spring Boot configuration; distinguish extraction from runtime settings. |
| [username-anarchy](skills/username-anarchy/SKILL.md) | Name-preserving username candidate generation and format selection. |
| [vault](skills/vault/SKILL.md) | Inspect Vault status and SSH OTP roles; distinguish policy, credential issuance and remote login. |
| [vim](skills/vim/SKILL.md) | Controlled inspection, literal substitutions and copied-swap recovery with startup/format limits. |
| [vtysh](skills/vtysh/SKILL.md) | Diagnose FRR/Quagga BGP sessions, prefix selection and advertisement policy against forwarding evidence. |
| [wfuzz](skills/wfuzz/SKILL.md) | HTTP path/host/Origin, form/cookie and server-side socket comparisons with meaningful controls and coverage. |
| [wget](skills/wget/SKILL.md) | Selected artifact retrieval, output/response evidence and resume pitfalls. |
| [whatweb](skills/whatweb/SKILL.md) | Fingerprint a selected HTTP response, bound redirects/aggression and distinguish plugin evidence from vulnerability claims. |
| [whoami](skills/whoami/SKILL.md) | Read the effective Linux user name with GNU whoami. Use to identify the current execution context without confusing a prompt or account name with real UID or Windows token privileges. |
| [whois](skills/whois/SKILL.md) | Query explicit registration sources and interpret referrals, redactions and differences from live DNS. |
| [windapsearch](skills/windapsearch/SKILL.md) | Inspect AD users/custom attributes with legacy Python syntax and correct visibility, encoding and exit-status interpretation. |
| [wpscan](skills/wpscan/SKILL.md) | Scope WordPress plugin/user inventory and distinguish detection, account access and incomplete vulnerability evidence. |
| [wrapwrap](skills/wrapwrap/SKILL.md) | Generate PHP resource-wrapper chains and validate envelope, byte transformations and consumer limits. |
| [xml-pp](skills/xml-pp/SKILL.md) | Format trusted XML while retaining original bytes, parse failures and entity-handling limits. |
| [xxd](skills/xxd/SKILL.md) | Inspect and reconstruct exact bytes; distinguish offsets, patching, hex representation and text encoding. |
| [ysoserial](skills/ysoserial/SKILL.md) | Generate selected Java serialization fixtures without confusing producer failures, binary output and target effects. |
| [yubisim](skills/yubisim/SKILL.md) | Generate an authorized Yubico OTP while preserving token counters and distinguishing output from validator acceptance. |
| [zip](skills/zip/SKILL.md) | Package selected source/data trees with deliberate recursion, exclusions, Unix symlink handling and member/integrity checks. |

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
