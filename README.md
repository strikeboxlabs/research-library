# Research library

**Start with [GETTING_STARTED.md](GETTING_STARTED.md)** for the Linux checkout, installation, host adaptation and creating skills from documentation.

This repository contains independent Linux tool skills and the existing [Arcanum-inspired LLM assessment methodology](methodologies/arcanum-llm-assessment.md).

## Tool skills

Skills supply tool selection and on-demand operational knowledge for capable CLI agents on the Linux distribution/image we deploy and control. A later pass on that image will add verified binary paths and relevant environment facts to the references. Each tool has its own `skills/<name>/SKILL.md`. Copy or link only the folders a worker needs; every skill works independently of the rest of this repository.

| Skill | Current scope |
|---|---|
| [7z](skills/7z/SKILL.md) | Inspect/extract archives and disk images; diagnose backup format, listfile, wildcard and symlink boundaries. |
| [adb](skills/adb/SKILL.md) | Inspect a selected Android device, install an owned APK by package ID and separate reverse routing, proxy and CA trust. |
| [adduser](skills/adduser/SKILL.md) | Provision an approved local account and verify primary groups, configured hooks, partial creation and effective privilege. |
| [aircrack-ng](skills/aircrack-ng/SKILL.md) | Inspect saved WPA/WPA2 network and handshake metadata without dictionary or radio actions. |
| [ansible-galaxy](skills/ansible-galaxy/SKILL.md) | Inspect selected local role paths, reported versions, configuration and inventory gaps. |
| [ansible-parallel](skills/ansible-parallel/SKILL.md) | Run explicit independent playbooks concurrently; retain each host recap and diagnose input/status gaps. |
| [ansible-vault](skills/ansible-vault/SKILL.md) | Extract and decrypt vault objects without loading playbooks or confusing vault passwords with plaintext values. |
| [apktool](skills/apktool/SKILL.md) | Decode APK resources, resolve framework gaps and distinguish a rebuild from valid Android signing. |
| [apport-cli](skills/apport-cli/SKILL.md) | Collect/view selected Apport reports and assess privileged pager behavior with full package, terminal and child-identity evidence. |
| [apt](skills/apt/SKILL.md) | Review and perform one selected interactive APT installation; distinguish planned and actual dependency changes. |
| [apt-get](skills/apt-get/SKILL.md) | Plan and perform a selected package installation; distinguish simulation, dependency changes and actual installer completion. |
| [ar](skills/ar/SKILL.md) | List acquired archives and extract a selected Debian-package member without installing or executing it. |
| [aureport](skills/aureport/SKILL.md) | Interpret existing TTY audit records and correlate events without misattributing copied logs. |
| [awk](skills/awk/SKILL.md) | Separate program source, literal data and regexes; recognize quoted CSV and binary-transfer limits. |
| [aws](skills/aws/SKILL.md) | Inspect explicit S3/DynamoDB/Lambda endpoints, bound bucket/object reads and interpret pagination, keys and version-qualified function metadata. |
| [az](skills/az/SKILL.md) | Inspect and download selected Azure/Azurite blobs with explicit endpoint, identity and transfer verification. |
| [backy](skills/backy/SKILL.md) | Run an archive-only JSON task and distinguish skipped cycles, destructive sync options and verified backup output. |
| [base64](skills/base64/SKILL.md) | Preserve transferred bytes and distinguish digest bytes, base64url and HTTP form-encoding layers. |
| [basename](skills/basename/SKILL.md) | Derive a selected path component or exact suffix while preserving quoting and output-delimiter limits. |
| [bash](skills/bash/SKILL.md) | Diagnose startup, restricted sessions, pattern comparisons, data reparsing, environment inheritance, filename expansion and redirection order. |
| [bbot](skills/bbot/SKILL.md) | Select reconnaissance presets/modules, retain scan evidence and diagnose custom-module or privileged loader behavior. |
| [bee](skills/bee/SKILL.md) | Select Backdrop sites, inspect CLI context and evaluate PHP with understood process/sudo and artifact effects. |
| [binwalk](skills/binwalk/SKILL.md) | Identify embedded signatures, inspect entropy and extract selected data from firmware or binary files. |
| [bloodhound](skills/bloodhound/SKILL.md) | Import an acquired graph in the Legacy GUI and qualify object identities, permission edges and capture coverage. |
| [bloodhound-python](skills/bloodhound-python/SKILL.md) | Collect scoped AD directory evidence with BloodHound.py from Linux. Use when selecting CE versus legacy collectors, diagnosing Kerberos/DNS failures or distinguishing collected rights from current access. |
| [bloodyad](skills/bloodyad/SKILL.md) | Selected AD object reads, membership/owner changes and read-back with bloodyAD. |
| [bmap](skills/bmap/SKILL.md) | Inspect trailing filesystem slack with the legacy reader while preserving allocation and qualifying recovery evidence. |
| [bozohttpd](skills/bozohttpd/SKILL.md) | Interpret portable HTTP daemon routing and serve an owned static directory on loopback. |
| [bzip2](skills/bzip2/SKILL.md) | Recover one verified compression layer, preserving source bytes and partial/naming distinctions. |
| [capsh](skills/capsh/SKILL.md) | Inspect current capability sets, identity and securebits without confusing bounding entries or container root with operation success. |
| [cargo](skills/cargo/SKILL.md) | Existing Rust CLI builds/runs, selected target/profile and dependency-resolution limits. |
| [cast](skills/cast/SKILL.md) | Read Ethereum blocks, transactions and contract getters; distinguish ABI/state evidence from published transactions. |
| [cat](skills/cat/SKILL.md) | Read selected plaintext/configuration evidence and distinguish complete reads from filtered or transformed displays. |
| [certipy](skills/certipy/SKILL.md) | Enumerate AD CS configuration, request selected certificates, authenticate with a PFX, recover through a permitted key-credential write and update selected UPNs from Linux. Use to connect template/CA findings to enrollment prerequisites, issuance results and current certificate-mapping behavior. |
| [cewl](skills/cewl/SKILL.md) | Collect scoped website vocabulary with deliberate depth, filtering and plain-word output for offline audits. |
| [checksec](skills/checksec/SKILL.md) | Inspect ELF mitigation indicators with pwntools; separate artifact flags from runtime protection and identity. |
| [chisel](skills/chisel/SKILL.md) | Build and diagnose explicit Chisel port forwards or reverse SOCKS connections. Use when client/server direction, listener exposure, endpoint reachability or fingerprint authentication is unclear. |
| [chmod](skills/chmod/SKILL.md) | Selected Linux file mode and setuid-bit changes with verified ownership/access and execution limits. |
| [chntpw](skills/chntpw/SKILL.md) | List Windows local accounts and edit selected SAM account settings on an offline hive copy. |
| [chown](skills/chown/SKILL.md) | Change one selected file's owner/group and verify numeric ownership separately from effective access. |
| [cmake](skills/cmake/SKILL.md) | Configure and build reviewed projects with explicit source/build trees and separate cache, artifact and installation results. |
| [composer](skills/composer/SKILL.md) | PHP dependency/lock inspection, selected installs and project-script execution context. |
| [consul](skills/consul/SKILL.md) | Inspect selected KV data, distinguish ACL permissions and validate configuration before reload decisions. |
| [convert](skills/convert/SKILL.md) | Crop raster pixels or generate a marked PDF with ImageMagick 6; distinguish canvas, font and coder-policy failures. |
| [cp](skills/cp/SKILL.md) | Copy selected files/directories and verify bytes, ownership, path and metadata differences. |
| [credentialmanager](skills/credentialmanager/SKILL.md) | Read a selected stored Windows credential through the installed CredentialManager PowerShell module in a remote session. Use from a Linux worker when network-logon or SYSTEM context differs from the intended user credential set. |
| [crontab](skills/crontab/SKILL.md) | Read the current user's schedule and distinguish configuration, missing tables and execution gaps. |
| [crunch](skills/crunch/SKILL.md) | Generate a small owned text fixture with explicit pattern alphabets, calculated size and completed-output checks. |
| [cryptsetup](skills/cryptsetup/SKILL.md) | Inspect LUKS, verify a known passphrase, and unlock image copies with read-only mappings and filesystem-aware mounting. |
| [curl](skills/curl/SKILL.md) | Capture HTTP evidence and interpret API, URL-checker, stored-template, protocol and encoding boundaries. |
| [cut](skills/cut/SKILL.md) | Project known delimiter-separated fields and retain delimiterless, empty-field and producer coverage limits. |
| [date](skills/date/SKILL.md) | Format established epoch seconds or a job's current date with explicit timezone and retain time-evidence limits. |
| [dd](skills/dd/SKILL.md) | Acquire identified offline block images and extract measured byte ranges; verify size, overwrite protection and consistency limits. |
| [de4dot](skills/de4dot/SKILL.md) | Prepare a separate owned .NET assembly for decompilation with build, execution and symbol-recovery limits. |
| [derby-ij](skills/derby-ij/SKILL.md) | Inspect consistent Derby copies with embedded JDBC, schema discovery, bounded SQL and understood display/lock limits. |
| [df](skills/df/SKILL.md) | Inspect the selected path's filesystem capacity with explicit units and mount/access limits. |
| [diff](skills/diff/SKILL.md) | Compare acquired trees or application variants and trace added commands, guards, paths and deployment assumptions. |
| [dig](skills/dig/SKILL.md) | Query explicit DNS servers, TXT/SPF text and approved transfers; distinguish resolver views, policy data and completeness. |
| [dirbuster](skills/dirbuster/SKILL.md) | Discover selected web paths using the headless CLI, explicit wordlists and controlled expansion; preserve report/completion and confirm real routes. |
| [dirsearch](skills/dirsearch/SKILL.md) | Discover scoped web paths; narrow partial-name candidates and handle expansion, soft 404s and redirects. |
| [dive](skills/dive/SKILL.md) | Inspect local image layers, distinguish deletion markers and recover selected historical file bytes. |
| [dnstool](skills/dnstool/SKILL.md) | Query, add and remove a selected AD-integrated DNS A record with krbrelayx dnstool from Linux. Use to distinguish LDAP bind, DNS-node permissions, stored changes and actual DNS resolution. |
| [doas](skills/doas/SKILL.md) | Match existing policy and execute an authorized command as its configured target identity. |
| [docker](skills/docker/SKILL.md) | Pinned tool environments, selected container exec/device access, mount attribution, registry/source inspection and image/archive transfer. |
| [docker-compose](skills/docker-compose/SKILL.md) | Resolve/run an explicit project and diagnose capability grants, privileged wrappers and cleanup effects. |
| [docker-registry-grabber](skills/docker-registry-grabber/SKILL.md) | Retrieve selected legacy image blobs from an owned loopback registry and verify tag/layer limits. |
| [dotnet](skills/dotnet/SKILL.md) | Distinguish .NET Framework/platform targets, select SDK/runtime context and build or run reviewed projects explicitly. |
| [dpkg](skills/dpkg/SKILL.md) | Query one package's installed state and audit partial configuration without treating an install command as completion. |
| [dpkg-deb](skills/dpkg-deb/SKILL.md) | Build/inspect Debian archives and retain control-hook, ownership and privileged-installer boundaries. |
| [dpkg-query](skills/dpkg-query/SKILL.md) | Match file ownership, installed state and complete Debian/Ubuntu package versions to the applicable vendor advisory. |
| [ebook-convert](skills/ebook-convert/SKILL.md) | Convert e-books with explicit formats and diagnose resource inclusion and transformation stages. |
| [emulator](skills/emulator/SKILL.md) | Start an owned Android AVD with selected DNS settings and separate guest resolution, proxy and TLS outcomes. |
| [enum4linux](skills/enum4linux/SKILL.md) | Read selected SMB share or domain password-policy metadata with classic enum4linux; preserve helper and effective-access limits. |
| [env](skills/env/SKILL.md) | Compare a trusted diagnostic with a deliberately cleared environment and retain runtime/terminal prerequisites. |
| [enyx](skills/enyx/SKILL.md) | Read selected SNMP IPv6 address indices with the legacy wrapper; verify parser failures and inaccurate class labels against raw rows. |
| [evil-winrm](skills/evil-winrm/SKILL.md) | Open a Windows WinRM session from Linux with Evil-WinRM using known credentials. Use for transport/authentication diagnosis, current token inspection, selected file transfers and distinguishing WinRM access from SMB login success. |
| [evil-winrm-py](skills/evil-winrm-py/SKILL.md) | Verify an authorized WinRM session with an existing Kerberos cache; read identity and selected registry metadata, preserving implementation and TLS limits. |
| [evtx2json](skills/evtx2json/SKILL.md) | Export selected acquired EVTX records with parser, resource-path and logon-correlation limits. |
| [exiftool](skills/exiftool/SKILL.md) | Read image/document metadata while preserving tag groups and treating identities as leads. |
| [fail2ban-client](skills/fail2ban-client/SKILL.md) | Trace failures through jails, filters and actions; diagnose bans and perform selected unban/reload operations. |
| [fakedns](skills/fakedns/SKILL.md) | Serve scoped synthetic DNS answers and reproduce query-count rebinding with resolver/cache evidence. |
| [featherduster](skills/featherduster/SKILL.md) | Analyze owned local sample encodings and statistical properties while preserving import boundaries and heuristic limits. |
| [feh](skills/feh/SKILL.md) | Classify/load selected local images with the installed decoders; distinguish readable pixels from a format label. |
| [feroxbuster](skills/feroxbuster/SKILL.md) | Bound web discovery and interpret wildcard filters, parent-directory denial, accessible children and incomplete scans. |
| [ffuf](skills/ffuf/SKILL.md) | Compare scoped paths, virtual hosts and account aliases using controls, budgets and meaningful response differences. |
| [fickling](skills/fickling/SKILL.md) | Inspect pickle streams statically and distinguish findings, scanner failures and incomplete model coverage. |
| [file](skills/file/SKILL.md) | Classify artifacts without confusing format labels, managed assemblies, transfer integrity and runtime compatibility. |
| [find](skills/find/SKILL.md) | Scope searches and timestamp inventories while interpreting permissions, emptiness, traversal errors and action boundaries. |
| [findmnt](skills/findmnt/SKILL.md) | Identify covering filesystems and exact mountpoints while preserving namespace and host-source uncertainty. |
| [firefox-decrypt](skills/firefox-decrypt/SKILL.md) | Recover saved logins from one authorized offline Mozilla profile; diagnose key/NSS compatibility and incomplete records. |
| [flask](skills/flask/SKILL.md) | Serve owned form/browser-test routes and separate POST receipt, assets, opener navigation and authentication evidence. |
| [flask-unsign](skills/flask-unsign/SKILL.md) | Decode an acquired Flask session locally and distinguish readable claims, encoding and signature verification. |
| [forge](skills/forge/SKILL.md) | Diagnose Foundry builds with explicit project/compiler context and correctly interpreted helper trace logs. |
| [ftp](skills/ftp/SKILL.md) | Transfer selected files, diagnose data channels and verify an authorised upload-to-web mapping without inferring code execution. |
| [gawk](skills/gawk/SKILL.md) | Deduplicate one owned text file with GNU inplace, first-seen order and a preserved backup. |
| [gcc](skills/gcc/SKILL.md) | Compile selected C tools/shared libraries; distinguish build stages, ABI, declarations and runtime compatibility. |
| [gdb](skills/gdb/SKILL.md) | Inspect matching core/live state and distinguish controlled instruction changes from ordinary program behavior. |
| [gdbserver](skills/gdbserver/SKILL.md) | Debug controlled remote programs over SSH with understood transport, connection modes and process lifetime. |
| [gem](skills/gem/SKILL.md) | Inspect exact installed RubyGem versions in the intended environment and distinguish inventory from application loading. |
| [getcap](skills/getcap/SKILL.md) | Verify file capabilities and distinguish stored flags, execution conditions and current process authority. |
| [getent](skills/getent/SKILL.md) | Resolve NSS users/groups and distinguish directory membership from current process privileges. |
| [getfacl](skills/getfacl/SKILL.md) | Explain POSIX ACL masks, named identities, parent traversal and default inheritance for access failures. |
| [ghidra](skills/ghidra/SKILL.md) | Headless selected decompilation, bounded mapped bytes and Rust cipher/comparison or database/file data-flow analysis. |
| [git](skills/git/SKILL.md) | Inspect repository evidence, offline bundles, typed objects, historical files and local reflogs, stored modes, patches and local hooks. |
| [git-dumper](skills/git-dumper/SKILL.md) | Recover exposed Git data within an isolated environment and distinguish missing objects, checkout failures and incomplete history. |
| [gluster](skills/gluster/SKILL.md) | Read named Gluster volume topology through the management CLI; distinguish brick metadata from client access. |
| [go](skills/go/SKILL.md) | Build reviewed CLI projects; resolve generated imports and distinguish command construction, execution and unchecked results. |
| [gobuster](skills/gobuster/SKILL.md) | Discover web paths and HTTP virtual hosts with version-aware hostname construction, filters and redirect controls. |
| [gpg](skills/gpg/SKILL.md) | Decrypt a selected OpenPGP backup with GnuPG using its known passphrase or matching secret key. Use to distinguish symmetric encryption, key material, pinentry behavior and partial plaintext from a valid recovery. |
| [gpp-decrypt](skills/gpp-decrypt/SKILL.md) | Decode captured GPP cpassword values; distinguish the Ruby and Python implementations. |
| [grafana2hashcat](skills/grafana2hashcat/SKILL.md) | Convert verified historical Grafana records with iamaldiâ€™s installed converter; preserve literal salts, cost, row mapping and full-verifier interpretation. |
| [grep](skills/grep/SKILL.md) | Filter text or readable log trees with exact match/error semantics and interpret misplaced credential candidates. |
| [groups](skills/groups/SKILL.md) | Inspect the current Linux process group names or a selected account lookup with GNU groups. Use to distinguish live session membership from directory membership and application authorization. |
| [grpc-tools-protoc](skills/grpc-tools-protoc/SKILL.md) | Generate local Python protobuf/gRPC bindings with explicit schema roots and output/runtime evidence. |
| [grpcurl](skills/grpcurl/SKILL.md) | Discover selected gRPC schemas and issue established read-only RPCs with distinct transport, message and metadata evidence. |
| [gzip](skills/gzip/SKILL.md) | Recover selected gzip streams; interpret suffixes, concatenation and failed integrity checks. |
| [h2csmuggler](skills/h2csmuggler/SKILL.md) | Distinguish h2c upgrade acceptance, tunneled application replies and actual access-control differences. |
| [hash-identifier](skills/hash-identifier/SKILL.md) | Classify checksum format candidates and distinguish heuristic ordering from a proven algorithm. |
| [hashcat](skills/hashcat/SKILL.md) | Bound offline checks/candidate generation and preserve Django/Grafana/Gitea PBKDF2, salts, binary inputs and result limits. |
| [hashid](skills/hashid/SKILL.md) | Identify candidate hash formats offline and handle ambiguous matches, unsupported prefixes and format hints. |
| [head](skills/head/SKILL.md) | Preview selected text-file beginnings while retaining file identity and partial-read limits. |
| [hostname](skills/hostname/SKILL.md) | Identify configured namespace-local addresses and distinguish DNS, address order and reachability. |
| [httpie](skills/httpie/SKILL.md) | Construct JSON API requests offline and interpret selected lookups with explicit input and status handling. |
| [hydra](skills/hydra/SKILL.md) | Perform scoped protocol/form authentication tests with bounded attempts and verified response classification. |
| [iconv](skills/iconv/SKILL.md) | Convert captured text with explicit encodings; distinguish UTF-16 byte order, terminators and lossy recovery. |
| [id](skills/id/SKILL.md) | Verify real/effective user/group IDs in the current context and distinguish named-account lookup from execution privilege. |
| [identify](skills/identify/SKILL.md) | Inspect one selected image's format, geometry and metadata while separating signatures and header reads from complete validation. |
| [ifconfig](skills/ifconfig/SKILL.md) | Inspect local interface addresses, flags and counters while retaining active-only and namespace limits. |
| [iis-shortname-scanner](skills/iis-shortname-scanner/SKILL.md) | Check IIS short-name disclosure and distinguish partial aliases, response ambiguity and confirmed full paths. |
| [ike-scan](skills/ike-scan/SKILL.md) | Interpret an IKE endpoint's initial proposal response, notify errors and vendor fingerprints without claiming authentication. |
| [ilspycmd](skills/ilspycmd/SKILL.md) | Inspect .NET types, time-seeded crypto, serialization and archive-write paths without launching the assembly. |
| [imap-enumeration](skills/imap-enumeration/SKILL.md) | Inspect IMAP capabilities and selected mailbox/session evidence. |
| [impacket-addcomputer](skills/impacket-addcomputer/SKILL.md) | Selected AD computer-account creation, method differences and owned cleanup. |
| [impacket-dacledit](skills/impacket-dacledit/SKILL.md) | Inspect/back up DACLs, apply precise delegation and verify ACE removal or restoration without losing concurrent state. |
| [impacket-getadusers](skills/impacket-getadusers/SKILL.md) | Query selected AD user metadata and interpret filtering, email requirements and DC-local logon dates. |
| [impacket-getnpusers](skills/impacket-getnpusers/SKILL.md) | Check selected accounts for AS-REP material without password guessing. |
| [impacket-getst](skills/impacket-getst/SKILL.md) | Request selected Kerberos service tickets and interpret SPNs, existing delegation and saved cache identity. |
| [impacket-gettgt](skills/impacket-gettgt/SKILL.md) | Obtain a Kerberos file credential cache using known credentials with Impacket getTGT. Use when Linux LDAP or SMB clients need a ticket and cache identity, hostname or clock errors interrupt authentication. |
| [impacket-getuserspns](skills/impacket-getuserspns/SKILL.md) | Separate SPN enumeration from selected service-ticket requests for an offline audit. |
| [impacket-lookupsid](skills/impacket-lookupsid/SKILL.md) | Resolve bounded RID ranges while preserving SID scope, principal types and incomplete-lookup evidence. |
| [impacket-mssqlclient](skills/impacket-mssqlclient/SKILL.md) | Inspect SQL authentication, cache/SPN selection, SQL identity, linked-server definitions, command configuration and one approved local service directory. |
| [impacket-ntlmrelayx](skills/impacket-ntlmrelayx/SKILL.md) | Configure a selected NTLM relay with Impacket and distinguish inbound authentication, target authentication and the chosen protocol action. Use for controlled relay testing with explicit listeners, destinations and result evidence. |
| [impacket-owneredit](skills/impacket-owneredit/SKILL.md) | Exact AD owner SID read/write and restoration constraints. |
| [impacket-psexec](skills/impacket-psexec/SKILL.md) | Execute selected Windows commands through Impacket services and distinguish authentication, execution and cleanup. |
| [impacket-reg](skills/impacket-reg/SKILL.md) | Query selected remote registry keys while accounting for hive context and service-state changes. |
| [impacket-rpcmap](skills/impacket-rpcmap/SKILL.md) | Distinguish scoped RPC interface binding, automatic fallback probes and actual method calls. |
| [impacket-secretsdump](skills/impacket-secretsdump/SKILL.md) | Parse existing Windows SAM/SYSTEM, SECURITY or NTDS snapshots, perform approved remote member-host acquisition or a selected-account AD replication audit with Impacket secretsdump. Use to distinguish offline evidence, current credentials and incomplete results. |
| [impacket-smbclient](skills/impacket-smbclient/SKILL.md) | Impacket SMB share/file operations with independent authentication and transfer guidance. |
| [impacket-smbexec](skills/impacket-smbexec/SKILL.md) | Run selected Windows commands through the Service Control Manager with Impacket smbexec from Linux. Use when SMB administrative access exists and service execution, output shares or SYSTEM versus user context matters. |
| [impacket-smbserver](skills/impacket-smbserver/SKILL.md) | Run a temporary bound SMB transfer share with explicit authentication and verified file transfer. |
| [impacket-ticketconverter](skills/impacket-ticketconverter/SKILL.md) | Convert owned single-ticket kirbi/FILE cache artifacts offline; verify metadata and multi-ticket loss limits. |
| [impacket-ticketer](skills/impacket-ticketer/SKILL.md) | Generate and inspect selected Kerberos service tickets with known service keys with Impacket ticketer. Use to distinguish service keys, SPNs, identity fields, cache creation and actual service acceptance in an authorized lab. |
| [impacket-wmiexec](skills/impacket-wmiexec/SKILL.md) | WMI/DCOM command execution, SMB output stages and cleanup interpretation. |
| [inotifywait](skills/inotifywait/SKILL.md) | Observe bounded local filesystem events and distinguish creation, write closure, moves and exact pathname handling. |
| [inveigh](skills/inveigh/SKILL.md) | Capture a bounded selected HTTP NTLM authentication exchange with cross-platform Inveigh. Use when an application sends outbound integrated authentication and identity, listener exposure or challenge-response interpretation needs evidence. |
| [ip](skills/ip/SKILL.md) | Explain Linux route selection using local addresses, policy rules, prefix specificity and namespace-aware lookups. |
| [ipcs](skills/ipcs/SKILL.md) | Inspect System V shared-memory metadata, keys, segment IDs, permissions and namespace limits. |
| [ipfs](skills/ipfs/SKILL.md) | Inspect local Kubo blocks, resolve UnixFS roots and recover selected files without fetching from peers. |
| [ipset](skills/ipset/SKILL.md) | Inspect kernel set types/members and compare ban exports with actual membership and firewall policy. |
| [iptables](skills/iptables/SKILL.md) | Inspect firewall backend, family and packet path with ordered rules, state, source/destination ports and saved-versus-live limits. |
| [iptables-save](skills/iptables-save/SKILL.md) | Capture ruleset evidence while distinguishing output-file effects, coverage, restore and persistence. |
| [irb](skills/irb/SKILL.md) | Evaluate reviewed local Ruby expressions and distinguish complete-string validation, match offsets and deployed behavior. |
| [irssi](skills/irssi/SKILL.md) | Inspect one approved IRC registration reply and distinguish notices, welcome and version claims. |
| [jadx](skills/jadx/SKILL.md) | Inspect APK resources and DEX call paths while recovering from incomplete decompilation. |
| [jar](skills/jar/SKILL.md) | Inspect/create archives from reviewed staging trees or replace one resource while preserving member and signature/runtime limits. |
| [jarsigner](skills/jarsigner/SKILL.md) | Sign an owned archive copy or interpret JAR coverage, strict warnings and Android verifier boundaries. |
| [java](skills/java/SKILL.md) | Launch a selected Java CLI with explicit runtime/classpath and distinguish missing classes from application failure. |
| [javac](skills/javac/SKILL.md) | Compile reviewed Java sources into a controlled output tree and diagnose release/API/processor differences. |
| [jdb](skills/jdb/SKILL.md) | Attach to a JVM, reach relevant breakpoints and inspect suspended frames with understood evaluation effects. |
| [jenkins-cli](skills/jenkins-cli/SKILL.md) | Verify controller identity/permissions and inspect an existing build log; distinguish transports, local authentication files and historical disclosure evidence. |
| [jenkins-offline-decrypt](skills/jenkins-offline-decrypt/SKILL.md) | Matched-backup Jenkins Secret recovery and implementation/parser limits. |
| [jjs](skills/jjs/SKILL.md) | Run a trusted legacy Nashorn script and distinguish engine availability, Java class access, arguments and child results. |
| [john](skills/john/SKILL.md) | Run bounded offline checks with John the Ripper Jumbo on NT, NetNTLMv2, Kerberos, ZIP, KeePass, OpenPGP secret keys, bcrypt, phpass, raw MD5/SHA-256, sha512crypt or HS256 JWT artifacts. Use to choose formats, preserve records and interpret session results. |
| [jq](skills/jq/SKILL.md) | Preserve JSON types, select decoded account maps and construct requests/config transformations without corrupting evidence. |
| [jwt-tool](skills/jwt-tool/SKILL.md) | Inspect/check/sign controlled JWTs, including scoped InfluxDB v1 HMAC candidates, without conflating claims and application access. |
| [keepassxc-cli](skills/keepassxc-cli/SKILL.md) | Inspect a database with known unlock factors and retrieve exact entries/fields without broad disclosure. |
| [kerbrute](skills/kerbrute/SKILL.md) | Check a bounded candidate username list against a selected KDC and interpret incomplete results. |
| [keytool](skills/keytool/SKILL.md) | Inspect a selected keystore alias or create an owned test signing identity with explicit trust and key limits. |
| [kill](skills/kill/SKILL.md) | Signal one identified owned process or Bash job and verify exit separately from the signal request. |
| [kinit](skills/kinit/SKILL.md) | Obtain MIT Kerberos tickets in an explicit cache, including existing-certificate PKINIT. |
| [klist](skills/klist/SKILL.md) | Inspect a selected MIT Kerberos credential cache from Linux. Use to verify principal, realm, service and expiry before a client login, without confusing a cached ticket with application authorization. |
| [kpcli](skills/kpcli/SKILL.md) | Open a known authorized KeePass database and inspect its group/entry inventory without saving changes. |
| [krbrelayx](skills/krbrelayx/SKILL.md) | Relay a selected Kerberos authentication exchange to an AD CS web endpoint with krbrelayx from Linux. Use when NTLM is unavailable and callback DNS naming, SPN selection, listener routing and certificate identity need explicit evidence. |
| [kubectl](skills/kubectl/SKILL.md) | Inspect scoped Kubernetes resources and create or execute in one approved Pod with context and RBAC evidence. |
| [ldapsearch](skills/ldapsearch/SKILL.md) | Query AD or POSIX identities, groups, deleted objects and policy with explicit schema, authentication and coverage. |
| [ldapwhoami](skills/ldapwhoami/SKILL.md) | Verify the server-returned LDAP authorization identity with the selected existing GSSAPI context. |
| [ldbsearch](skills/ldbsearch/SKILL.md) | Inspect records in an offline SSSD LDB cache while preserving identity and attribute context. Use when strings output cannot map a value to an account or a cache query appears empty. |
| [ldconfig](skills/ldconfig/SKILL.md) | Inspect/refresh library caches and exercise a scoped writable-directory load with actual identity evidence. |
| [ldd](skills/ldd/SKILL.md) | Resolve trusted ELF dependencies and distinguish missing objects, unexpected paths and privileged-launch limits. |
| [less](skills/less/SKILL.md) | Inspect literal text and assess a selected pager child without confusing wrapping, secure mode or parent privilege. |
| [lftp](skills/lftp/SKILL.md) | Use verified explicit FTPS for selected transfers and diagnose transport, data-channel and virtual-user access differences. |
| [linpeas](skills/linpeas/SKILL.md) | Scope enumeration checks and verify unfamiliar SUID helpers, execution conditions and vendor package evidence. |
| [ln](skills/ln/SKILL.md) | Create a selected owned symbolic link with exact destination and target-resolution evidence. |
| [logrotate](skills/logrotate/SKILL.md) | Preview actual rotation jobs and interpret state, skip conditions, permissions and hook identities. |
| [logrotten](skills/logrotten/SKILL.md) | Selected disposable-fixture logrotate race, path effects and write evidence. |
| [losetup](skills/losetup/SKILL.md) | Attach owned disk-image copies read-only, inspect partition devices and verify loop-device cleanup. |
| [ls](skills/ls/SKILL.md) | Inspect selected directory entries, hidden names and permission metadata while retaining namespace and timestamp limits. |
| [lsattr](skills/lsattr/SKILL.md) | Inspect selected filesystem attributes and distinguish append-only/immutable flags from file modes. |
| [lsblk](skills/lsblk/SKILL.md) | Inspect block-device relationships and mount views without confusing whole disks, partitions or host provenance. |
| [ltrace](skills/ltrace/SKILL.md) | Observe dynamic library calls in owned unprivileged programs; interpret incomplete traces and argument values. |
| [magick](skills/magick/SKILL.md) | Identify the trusted ImageMagick 7 build, declared formats, delegates and policy with service-context limits. |
| [mail](skills/mail/SKILL.md) | Distinguish GNU Mailutils and S-nail flags, subject handling, attachments and submission evidence. |
| [make](skills/make/SKILL.md) | Build reviewed existing tool targets; diagnose configured features, compiler failures and stale artifacts without implying installation. |
| [marshalsec](skills/marshalsec/SKILL.md) | Select unmarshalling fixtures and distinguish local test execution, JNDI stages and runtime dependencies. |
| [masscan](skills/masscan/SKILL.md) | Discover scoped TCP/UDP responders with explicit configuration and host/protocol-preserving service follow-up. |
| [mcs](skills/mcs/SKILL.md) | Compile trusted C# with explicit sources, references and output kind; separate language features from runtime proof. |
| [md5sum](skills/md5sum/SKILL.md) | Reproduce exact legacy checksum bytes and distinguish malformed, missing or mismatching manifests. |
| [mdbtools](skills/mdbtools/SKILL.md) | Inventory and export selected Access database tables without corrupting field interpretation. |
| [memcached-tool](skills/memcached-tool/SKILL.md) | Inspect cache/slab statistics and bounded key/value exports with the existing protocol-aware helper. |
| [memprocfs](skills/memprocfs/SKILL.md) | Identify acquired Windows memory dumps on Linux with parser/system metadata and verified FUSE cleanup. |
| [minecraft-console-client](skills/minecraft-console-client/SKILL.md) | Use a headless Minecraft Java session and distinguish protocol support, offline identity, client commands and server responses. |
| [mingw-w64-gcc](skills/mingw-w64-gcc/SKILL.md) | Build a reviewed Windows C++ utility from Linux while distinguishing target, entrypoint, import libraries and runtime proof. |
| [mkdir](skills/mkdir/SKILL.md) | Create a selected owned working directory with deliberate modes and explicit existing-tree/cache limits. |
| [mktemp](skills/mktemp/SKILL.md) | Create an actual private temporary file in a chosen working parent and clean up its exact owned path. |
| [mogrify](skills/mogrify/SKILL.md) | Convert selected raster batches with explicit output paths, overwrite control and per-file verification. |
| [mongo](skills/mongo/SKILL.md) | Inspect known database/collection metadata with the legacy MongoDB shell and explicit authentication context. |
| [mosquitto-sub](skills/mosquitto-sub/SKILL.md) | Observe a selected ordinary MQTT topic with message/connection limits and retained/TLS distinctions. |
| [mount](skills/mount/SKILL.md) | Mount a selected block filesystem or known CIFS share; preserve access, namespace and cleanup evidence. |
| [mount-cifs](skills/mount-cifs/SKILL.md) | Mount SMB shares read-only; distinguish metadata timestamps, dialects, signing and local/server permissions. |
| [mount-nfs](skills/mount-nfs/SKILL.md) | Mount selected NFS exports read-only; diagnose version, identity, locking and mount-state evidence. |
| [msf-pattern](skills/msf-pattern/SKILL.md) | Pair Metasploit pattern generation and offset lookup without confusing heuristic matches or overwritten fields. |
| [msfconsole](skills/msfconsole/SKILL.md) | Select and configure Framework modules; manage matching handlers, jobs and sessions with explicit outcome checks. |
| [msfvenom](skills/msfvenom/SKILL.md) | Generate selected payload artifacts with matching platform, architecture, format and handler requirements. |
| [mv](skills/mv/SKILL.md) | Rename selected files with exact destinations, no-clobber completion and directory-permission distinctions. |
| [mvn](skills/mvn/SKILL.md) | Package a trusted Maven project and distinguish reactor failures, assembly output, stale artifacts and runtime success. |
| [mysql](skills/mysql/SKILL.md) | Explicit connection/account context, selected Joomla/Mattermost records, string semantics and native/client/server execution boundaries. |
| [mysqldump](skills/mysqldump/SKILL.md) | Back up a selected database and distinguish SQL failures, compression integrity, object coverage and validated recovery. |
| [named-checkconf](skills/named-checkconf/SKILL.md) | Check selected BIND configuration syntax and optional primary-zone loading; distinguish parse from live state. |
| [nano](skills/nano/SKILL.md) | Interactive selected-artifact editing, save and format verification |
| [nats](skills/nats/SKILL.md) | Inspect selected account/stream metadata and bounded stored messages; distinguish sequence reads from consumer-creating paging. |
| [nats-server](skills/nats-server/SKILL.md) | Run an owned loopback foreground server and verify one synthetic client exchange, trace effects and process cleanup. |
| [nc](skills/nc/SKILL.md) | Implementation-specific TCP exchanges, verified owned file transfers, selected-port checks, listeners and executable/FIFO process streams. |
| [ncat](skills/ncat/SKILL.md) | Exchange framed service data, capture callbacks, receive authorized two-way streams or inspect Memcached. |
| [neo4j](skills/neo4j/SKILL.md) | Start an owned DBMS with its existing process manager; distinguish launcher, server and client results. |
| [neo4j-admin](skills/neo4j-admin/SKILL.md) | Set the native database password before first startup; distinguish setup history from current database/OS credentials. |
| [neofetch](skills/neofetch/SKILL.md) | Display a local system summary with controlled configuration and honest field/exit-status interpretation. |
| [net](skills/net/SKILL.md) | Query SMB server time and perform an explicitly authorized local clock correction with Samba net. |
| [netexec](skills/netexec/SKILL.md) | Validate known SMB credentials, interpret share checks, read selected user metadata and inspect LDAP protection, AD CS endpoints and machine-account quota with NetExec on selected lab hosts. Use to avoid unintended credential combinations and distinguish authentication, password status, privilege indicators and path permissions. |
| [netpgp](skills/netpgp/SKILL.md) | Recover an owned OpenPGP backup with matching keys while distinguishing output errors and incomplete plaintext. |
| [netstat](skills/netstat/SKILL.md) | Linux TCP/UDP listeners, bound addresses and process visibility |
| [nginx](skills/nginx/SKILL.md) | Inspect selected configuration, proxy URI mapping, worker/file authority and WebDAV conditions with live-state evidence limits. |
| [nikto](skills/nikto/SKILL.md) | Survey a scoped web server for configuration and vulnerability candidates with Nikto. |
| [nimble](skills/nimble/SKILL.md) | Nim dependency inspection, selected provisioning and build-context diagnosis. |
| [nmap](skills/nmap/SKILL.md) | Keep protocol, address and IPsec vantage explicit; interpret service probes and uncertain states. |
| [node](skills/node/SKILL.md) | Resolve CommonJS dependencies, inspect request/signature control flow and perform selected bounded application tasks. |
| [npbackup-cli](skills/npbackup-cli/SKILL.md) | Select exact backup snapshots, recover a file and distinguish backend writes from wrapper policy/status failures. |
| [npm](skills/npm/SKILL.md) | Inspect an existing project or global package tree without install/script execution; interpret logical dependency results. |
| [nsupdate](skills/nsupdate/SKILL.md) | Add and remove one fresh owned A record with authenticated conditional DNS updates and authoritative verification. |
| [ntpdate](skills/ntpdate/SKILL.md) | Query a selected time server and distinguish observed offset, timing noise and clock-changing operations. |
| [oathtool](skills/oathtool/SKILL.md) | Generate known-secret TOTP and diagnose encoding, parameter and clock mismatches. |
| [objcopy](skills/objcopy/SKILL.md) | Extract a named ELF section into a fresh artifact without accidentally modifying the input object. |
| [objdump](skills/objdump/SKILL.md) | Inspect headers, imported calls and bounded disassembly while separating bytes, source lines and runtime evidence. |
| [omv-rpc](skills/omv-rpc/SKILL.md) | OpenMediaVault mounted-filesystem queries, local RPC privilege boundaries and selected installation/job output. |
| [openssl](skills/openssl/SKILL.md) | Inspect keys/certificates, TLS or ASN.1 objects and recover known-format CBC artifacts with explicit producer settings. |
| [openvpn](skills/openvpn/SKILL.md) | Use reviewed client profiles; distinguish tunnel initialization, selected routes, DNS and service reachability. |
| [pacman](skills/pacman/SKILL.md) | Inspect Arch package metadata, payloads, scriptlets and ownership before choosing an installation transaction. |
| [passpie](skills/passpie/SKILL.md) | Export an owned initialized vault with known decryption prerequisites, private plaintext output and verified coverage. |
| [passthecert](skills/passthecert/SKILL.md) | Python certificate LDAP authentication and selected RBCD change/read-back/removal. |
| [passwd](skills/passwd/SKILL.md) | Change a selected password interactively and separate password status from account access. |
| [patchelf](skills/patchelf/SKILL.md) | Inspect/change an owned ELF's loader and runtime library path with explicit working-directory and compatibility checks. |
| [pd4cmd](skills/pd4cmd/SKILL.md) | Convert reviewed HTML with PD4ML; diagnose entrypoints, resource access, layout and stale PDF output. |
| [pdftotext](skills/pdftotext/SKILL.md) | Extract acquired PDF text and diagnose page, layout, permission and missing-text coverage. |
| [peda](skills/peda/SKILL.md) | Load the installed GDB extension explicitly and correlate x86 registers, code, stack and call arguments. |
| [perl](skills/perl/SKILL.md) | Review producer results, literal file ingestion and compile-time effects with record and output-status limits. |
| [pgrep](skills/pgrep/SKILL.md) | Match visible process names and distinguish absence, lookup errors and service health. |
| [phantomjs](skills/phantomjs/SKILL.md) | Legacy CLI rendering, document capture and load/result interpretation. |
| [php](skills/php/SKILL.md) | Diagnose CLI/web context, exact legacy checksum inputs, validated process arguments and database/crypto tasks. |
| [phpggc](skills/phpggc/SKILL.md) | Select serialization chains by dependency and trigger; preserve bytes and validate the actual parser/object lifecycle. |
| [ping](skills/ping/SKILL.md) | Check one selected iputils ICMP echo path with a packet count, deadline and explicit reachability limits. |
| [pip](skills/pip/SKILL.md) | Match a Python/pip environment, retrieve reviewed wheels and inspect dependency/version or source-build boundaries. |
| [pret](skills/pret/SKILL.md) | Query selected PJL printer metadata and distinguish timeouts, revision gaps and startup effects. |
| [printerbug](skills/printerbug/SKILL.md) | Trigger one authorized Windows spooler RPC authentication callback with krbrelayx printerbug from Linux. Use to distinguish RPC bind, notification errors and independently observed NTLM or Kerberos backconnects. |
| [procyon](skills/procyon/SKILL.md) | Recover Java methods from local JAR/class files and trace plugin settings while qualifying reconstruction and runtime evidence. |
| [protoc](skills/protoc/SKILL.md) | Decode an acquired unframed Protocol Buffer body with its known schema and explicit format boundaries. |
| [proxychains](skills/proxychains/SKILL.md) | Route compatible Linux TCP clients through an explicit ProxyChains-NG configuration. Use when SOCKS or HTTP CONNECT policy, DNS behavior or unsupported raw/UDP traffic causes misleading failures. |
| [ps](skills/ps/SKILL.md) | Inspect process identity/state and targeted procfs evidence without confusing NUL-separated or mutable metadata. |
| [ps2pdf](skills/ps2pdf/SKILL.md) | Convert reviewed PostScript and diagnose status, template errors and Ghostscript file-access controls. |
| [pspy](skills/pspy/SKILL.md) | Correlate short-lived processes with jobs/actions while retaining exact paths, identities and visibility limits. |
| [psql](skills/psql/SKILL.md) | Inspect/export selected PostgreSQL/Django records and preserve SQL role, connection, server-file and archive-hook boundaries. |
| [pswm](skills/pswm/SKILL.md) | Retrieve selected vault aliases and recover compatible copied cryptocode stores without resetting the original. |
| [puttygen](skills/puttygen/SKILL.md) | Convert an existing authorized PuTTY key to OpenSSH and verify its public identity. |
| [pwntools](skills/pwntools/SKILL.md) | Complete framed exchanges, interpret timeouts/EOF and reconstruct integer fields with explicit widths and byte order. |
| [pygpoabuse](skills/pygpoabuse/SKILL.md) | Plan isolated lab GPO task tests with explicit commands, client scope, before-state and incomplete-cleanup handling. |
| [pyload](skills/pyload/SKILL.md) | Query a trusted installed pyLoad launcher's reported version and retain running-build association limits. |
| [pypykatz](skills/pypykatz/SKILL.md) | Inspect LSASS snapshots and derive known-password NT values while preserving identity and artifact type. |
| [python-http-server](skills/python-http-server/SKILL.md) | Serve selected local files or receive a bounded controlled POST callback with Python's http.server. Use when bind addresses, directory exposure, transfer verification or callback logs need interpretation. |
| [python2](skills/python2/SKILL.md) | Use existing Python 2.7 for raw-pickle or Django signed-cookie contracts and a selected Unix PTY child; distinguish generation, server effects and terminal authority. |
| [python3](skills/python3/SKILL.md) | Inspect owned Python data/code, diagnose local failures, query distribution metadata and use bounded transfer helpers. |
| [qpdf](skills/qpdf/SKILL.md) | List, extract and package selected owned PDF attachments while preserving keys, bytes and warning status. |
| [qrencode](skills/qrencode/SKILL.md) | Generate a QR image from selected bytes and distinguish artifact creation from decoded consumer acceptance. |
| [rdate](skills/rdate/SKILL.md) | Diagnose clock skew with print-only SNTP queries and distinguish protocol, timezone and synchronization issues. |
| [readelf](skills/readelf/SKILL.md) | Map ELF layouts and inspect dynamic dependencies/symbols while separating artifact metadata from runtime behavior. |
| [readlink](skills/readlink/SKILL.md) | Inspect stored symlink target text and distinguish canonical paths, missing components and changing referents. |
| [readpst](skills/readpst/SKILL.md) | Convert PST/supported OST mail while accounting for MIME, image attachments and conversion limits. |
| [recaf](skills/recaf/SKILL.md) | Inspect acquired Java archive classes and call paths with Recaf while preserving decompilation and deployment limits. |
| [redis-cli](skills/redis-cli/SKILL.md) | Inspect selected Redis values and effective persistence settings with known authentication, explicit databases and bounded cursor scans. |
| [remmina](skills/remmina/SKILL.md) | Launch an approved desktop URI or reviewed profile; verify graphical/plugin prerequisites and actual session outcome. |
| [responder](skills/responder/SKILL.md) | Separate name observation from active authentication listeners and preserve complete capture evidence. |
| [restic](skills/restic/SKILL.md) | Select backup snapshots/paths and restore into a new directory with understood helpers, filters and locks. |
| [rlwrap](skills/rlwrap/SKILL.md) | Local Readline editing for a selected client, with history and remote-terminal limits. |
| [rm](skills/rm/SKILL.md) | Remove one tracked owned file/link entry and distinguish directory failure, dangling links and object lifetime. |
| [ropgadget](skills/ropgadget/SKILL.md) | Inspect gadget candidates with understood search depth, address filters and complete instruction effects. |
| [roundcube](skills/roundcube/SKILL.md) | Inspect Roundcube webmail session, mailbox and deployed-application context. |
| [rpcclient](skills/rpcclient/SKILL.md) | Resolve RPC identities and perform selected SAMR account changes with distinct rights and outcome evidence. |
| [rpm](skills/rpm/SKILL.md) | Query the selected installed package build and reconcile distribution release/backport evidence. |
| [rsh](skills/rsh/SKILL.md) | GNU rsh command execution, rlogin fallback and legacy trust interpretation. |
| [rsync](skills/rsync/SKILL.md) | Inspect daemon modules, retrieve selected files or push a completed backup over SSH with explicit scope and transfer verification. |
| [ruby](skills/ruby/SKILL.md) | Identify the selected Ruby/Psych runtime and review version-dependent YAML loading and relative input paths. |
| [rustbuster](skills/rustbuster/SKILL.md) | Choose path, DNS, virtual-host or request-marker discovery with meaningful controls and filters. |
| [rustscan](skills/rustscan/SKILL.md) | Discover scoped TCP ports, tune resource/timeout behavior and hand findings to Nmap with separate evidence. |
| [samdump2](skills/samdump2/SKILL.md) | Extract matching legacy SAM/SYSTEM records and detect unsupported formats or misleading empty-password values. |
| [scp](skills/scp/SKILL.md) | Transfer selected files and recover from authentication, SFTP-subsystem, path or partial-copy failures. |
| [screen](skills/screen/SKILL.md) | Identify and resume sessions with understood sharing, ownership, terminal and multiuser requirements. |
| [script](skills/script/SKILL.md) | Allocate a util-linux PTY or capture a terminal session with correct exit/logging semantics. |
| [searchor](skills/searchor/SKILL.md) | Generate engine-specific search URLs and account for local history, browser and clipboard effects. |
| [searchsploit](skills/searchsploit/SKILL.md) | Search and inspect local exploit candidates without confusing title matches with applicability. |
| [sed](skills/sed/SKILL.md) | Review a suffix correction or remove a confirmed final record with GNU sed and an explicit backup. |
| [sendemail](skills/sendemail/SKILL.md) | Submit a reviewed message and attachment through an explicit SMTP relay and distinguish acceptance, transport policy and eventual delivery. |
| [sendmail](skills/sendmail/SKILL.md) | Submit requested messages with explicit envelope recipients and distinguish queue acceptance from delivery. |
| [seq](skills/seq/SKILL.md) | Generate bounded local integer lists and distinguish inclusive endpoints, step direction and generated counts from downstream completion. |
| [service](skills/service/SKILL.md) | Query or restart one selected service; preserve backend, action status and application-health evidence. |
| [setfacl](skills/setfacl/SKILL.md) | Change one owned file's POSIX ACL with a complete backup, computed-mask review and effective-rights verification. |
| [sftp](skills/sftp/SKILL.md) | Inspect an SFTP namespace, retrieve selected files or create owned symlinks; distinguish transport and application access. |
| [sha1sum](skills/sha1sum/SKILL.md) | Compare exact file bytes with legacy SHA-1 checksums; retain status and provenance limits. |
| [sha256sum](skills/sha256sum/SKILL.md) | Compute/verify selected file-byte SHA-256 checksums with manifest-path and read-status evidence. |
| [sharp-gpoabuse](skills/sharp-gpoabuse/SKILL.md) | Apply a selected GPO local-administrator change with SharpGPOAbuse through a remote Windows command session. Use from Linux to distinguish policy write rights, linked client scope, application and fresh token evidence. |
| [shocker](skills/shocker/SKILL.md) | Match a reviewed file-handle test build and qualify selected-file recovery and isolation prerequisites. |
| [showmount](skills/showmount/SKILL.md) | Inspect NFS export advertisements while distinguishing MOUNT-service limits, NFSv4 and actual access. |
| [sleep](skills/sleep/SKILL.md) | Apply a bounded GNU sleep delay and distinguish elapsed waiting from an observed readiness condition. |
| [smbclient](skills/smbclient/SKILL.md) | Retrieve selected SMB files with explicit identity and distinguish share labels, file permissions and execution evidence. |
| [smbmap](skills/smbmap/SKILL.md) | Inventory SMB access without default write probes and control traversal and selected downloads. |
| [smbpasswd](skills/smbpasswd/SKILL.md) | Change a known account's remote SMB password while distinguishing required changes, resets and local database operations. |
| [smtp-user-enum](skills/smtp-user-enum/SKILL.md) | Compare scoped SMTP recipient responses without treating tool classifications as mailbox proof. |
| [snap](skills/snap/SKILL.md) | Inspect revisions, confinement and change tasks; distinguish signature checks from executable install hooks. |
| [snmpwalk](skills/snmpwalk/SKILL.md) | Query bounded disk/process/hardware and IPv6 inventory, typed values and monitoring extensions with execution/visibility limits. |
| [sort](skills/sort/SKILL.md) | Sort and deduplicate selected records with explicit equality and sample-count semantics. |
| [splunkwhisperer2](skills/splunkwhisperer2/SKILL.md) | Authenticated remote Splunk app/script execution with callback routing, service identity, failed-response and cleanup interpretation. |
| [sponge](skills/sponge/SKILL.md) | Replace one owned file from a successful staged transformation; distinguish buffering and rollback. |
| [sqlcmd](skills/sqlcmd/SKILL.md) | Run a bounded SQL Server role query with known credentials and distinct SQL/integrated authentication evidence. |
| [sqlite3](skills/sqlite3/SKILL.md) | Inspect coherent SQLite copies and export selected Grafana verifier rows without confusing storage metadata, salt bytes or account mapping. |
| [sqlmap](skills/sqlmap/SKILL.md) | Test a selected HTTP parameter and inspect scoped database metadata or samples with request/session fidelity. |
| [ss](skills/ss/SKILL.md) | Inspect actual listeners/connections, address families, process visibility and namespaces. |
| [ssh](skills/ssh/SKILL.md) | Selected account/key login, application/chat commands, public-key enrollment, GSSAPI identity, loopback and dynamic SOCKS forwarding. |
| [ssh-keygen](skills/ssh-keygen/SKILL.md) | Generate selected key pairs, derive public fingerprints and validate complete transferred private-key artifacts. |
| [ssh-username-enum](skills/ssh-username-enum/SKILL.md) | Selected OpenSSH malformed-authentication account oracle with legacy-helper compatibility and control/result limits. |
| [sshpass](skills/sshpass/SKILL.md) | Provide selected SSH password input through a descriptor and distinguish prompt, key and authentication failures. |
| [sshuttle](skills/sshuttle/SKILL.md) | Selected service routing through an existing SSH identity, with Python/firewall prerequisites and cleanup evidence. |
| [sslscan](skills/sslscan/SKILL.md) | Enumerate supported TLS protocols, cipher suites and certificate details on a scoped endpoint. |
| [stat](skills/stat/SKILL.md) | Inspect a selected object's modification time with explicit symlink and timestamp limits. |
| [steghide](skills/steghide/SKILL.md) | Recover local embedded data with a known passphrase and explicit private output. |
| [stoken](skills/stoken/SKILL.md) | Import selected SecurID software tokens, generate codes and diagnose state/PIN/time differences. |
| [strace](skills/strace/SKILL.md) | Trace file/network failures and interpret acquired reads with process, descriptor, byte-count and tracing-side-effect context. |
| [strings](skills/strings/SKILL.md) | Triage binary files with GNU strings while retaining offsets and checking alternate encodings. Use when paths, error messages or UTF-16 text guide subsequent binary analysis. |
| [strongswan-ipsec](skills/strongswan-ipsec/SKILL.md) | Inspect existing VPN SAs and diagnose selector, transport-mode and application-path mismatches. |
| [stty](skills/stty/SKILL.md) | Inspect/save/restore terminal state and manage local relay echo/raw mode separately from a remote PTY. |
| [su](skills/su/SKILL.md) | Selected local account sessions with known credentials; login environment, PAM/terminal handling and effective-identity verification. |
| [sucrack](skills/sucrack/SKILL.md) | Bounded local su candidate checks; worker/rewrite choices, build features, prompt detection and independent account verification. |
| [sudo](skills/sudo/SKILL.md) | Interpret effective policy, program/helpers, authenticator/key-enrollment inputs and elevated operation results. |
| [swaks](skills/swaks/SKILL.md) | Preview MIME and diagnose explicit SMTP stages, TLS verification and delivery evidence. |
| [systemctl](skills/systemctl/SKILL.md) | Diagnose selected systemd units and apply validated reload/restart changes with useful outcome checks. |
| [tail](skills/tail/SKILL.md) | Read bounded log suffixes and follow selected writers across rotation/truncation with evidence limits. |
| [tar](skills/tar/SKILL.md) | Create plain or gzip packages with verified member layout, inspect/extract backups and diagnose filesystem boundaries. |
| [targetedkerberoast](skills/targetedkerberoast/SKILL.md) | Select existing-SPN or temporary-SPN ticket collection and verify directory state after write-enabled tests. |
| [tcpdump](skills/tcpdump/SKILL.md) | Capture scoped traffic at the correct interface/port, retain handshake evidence and distinguish application conclusions. |
| [tee](skills/tee/SKILL.md) | Copy stdin to stdout and selected files, including an authorized privileged append with truncation/error boundaries. |
| [telnet](skills/telnet/SKILL.md) | Inspect a known legacy text service; distinguish local client commands, application responses and connection evidence. |
| [text2wave](skills/text2wave/SKILL.md) | Generate speech fixtures while separating text normalization, audio output and downstream recognition. |
| [tftp](skills/tftp/SKILL.md) | Transfer selected files with tftp-hpa, explicit binary mode and independent completeness checks. |
| [thrift](skills/thrift/SKILL.md) | Generate reviewed RPC bindings and distinguish compiler, transport, protocol and handler outcomes. |
| [timedatectl](skills/timedatectl/SKILL.md) | Inspect clock/timezone and time-service state while distinguishing indicators from measured server offset. |
| [tmux](skills/tmux/SKILL.md) | Create and manage selected sessions/panes; preserve job context and distinguish detach from process termination. |
| [touch](skills/touch/SKILL.md) | Create a selected empty marker or update timestamps; distinguish no-op, symlink, content and provenance outcomes. |
| [tr](skills/tr/SKILL.md) | Translate selected separator bytes or remove confirmed single-field line wrapping without losing the original. |
| [tree](skills/tree/SKILL.md) | Inspect a selected directory layout with bounded depth; distinguish link scope, artifact names and incomplete listings. |
| [truncate](skills/truncate/SKILL.md) | Resize one selected owned regular file and verify size separately from pathname existence or log recovery. |
| [tshark](skills/tshark/SKILL.md) | Correlate saved FTP/TLS/Kerberos traffic with conversation identity, pre-authentication fields and incomplete evidence. |
| [tty](skills/tty/SKILL.md) | Identify stdin terminal endpoints and compare selected Unix session terminal sharing. |
| [ufw](skills/ufw/SKILL.md) | Add/remove one approved IPv6 TCP ingress rule on an active firewall; preserve baseline, effective-rule and service-connectivity evidence. |
| [uname](skills/uname/SKILL.md) | Read current kernel identity without confusing it with installed packages, login banners or vulnerability applicability. |
| [unbound-control](skills/unbound-control/SKILL.md) | Inspect resolver control/counters and change one live forwarding zone with verification and restoration. |
| [uniq](skills/uniq/SKILL.md) | Filter or count adjacent repeated records; distinguish global deduplication, ordering and projected identity limits. |
| [unzip](skills/unzip/SKILL.md) | Inspect ZIP names/CRCs and selected Spring Boot configuration; distinguish extraction from runtime settings. |
| [uptime](skills/uptime/SKILL.md) | Read uptime and 1/5/15-minute Linux load averages without inferring CPU percent or service health. |
| [useradd](skills/useradd/SKILL.md) | Provision one approved local account with explicit home, group and shell; verify partial state. |
| [username-anarchy](skills/username-anarchy/SKILL.md) | Name-preserving username candidate generation and format selection. |
| [users](skills/users/SKILL.md) | Read selected login records while distinguishing sessions, account existence, home-directory names and process identity. |
| [vault](skills/vault/SKILL.md) | Inspect Vault status and SSH OTP roles; distinguish policy, credential issuance and remote login. |
| [veracrypt](skills/veracrypt/SKILL.md) | Mount one owned container read-only with known credentials, verify its mapping and unmount only that volume. |
| [vim](skills/vim/SKILL.md) | Controlled inspection, literal substitutions and copied-swap recovery with startup/format limits. |
| [virtualenv](skills/virtualenv/SKILL.md) | Create a selected interpreter environment and verify executable/dependency context without relying on activation. |
| [vtysh](skills/vtysh/SKILL.md) | Diagnose FRR/Quagga BGP sessions, prefix selection and advertisement policy against forwarding evidence. |
| [wasm-decompile](skills/wasm-decompile/SKILL.md) | Inspect acquired Wasm as decompiler text; distinguish exports, inferred representations and later host actions. |
| [wat2wasm](skills/wat2wasm/SKILL.md) | Compile reviewed WAT to a fresh module and separate type/feature checks from host/runtime effects. |
| [watch](skills/watch/SKILL.md) | Observe selected read-only command output and distinguish sampled changes from a complete event log. |
| [wc](skills/wc/SKILL.md) | Count selected artifact bytes or newlines and distinguish representation size from integrity or record count. |
| [wfuzz](skills/wfuzz/SKILL.md) | HTTP path/host/Origin, form/cookie and server-side socket comparisons with meaningful controls and coverage. |
| [wget](skills/wget/SKILL.md) | Retrieve selected HTTP artifacts or approved FTP subtrees with transfer identity, mirror and page-capture evidence. |
| [whatweb](skills/whatweb/SKILL.md) | Fingerprint a selected HTTP response, bound redirects/aggression and distinguish plugin evidence from vulnerability claims. |
| [which](skills/which/SKILL.md) | Resolve a selected executable name on PATH and preserve implementation/version uncertainty. |
| [whoami](skills/whoami/SKILL.md) | Read the effective Linux user name with GNU whoami. Use to identify the current execution context without confusing a prompt or account name with real UID or Windows token privileges. |
| [whois](skills/whois/SKILL.md) | Query explicit registration sources and interpret referrals, redactions and differences from live DNS. |
| [windapsearch](skills/windapsearch/SKILL.md) | Inspect permitted AD user/group metadata with legacy Python windapsearch; distinguish direct membership from effective access. |
| [wine](skills/wine/SKILL.md) | Run a selected trusted Windows application in an explicit compatible Wine prefix and interpret runtime gaps. |
| [winetricks](skills/winetricks/SKILL.md) | Supply selected .NET Framework4.8 dependencies in a Wine prefix, separating install records and application results. |
| [wireshark](skills/wireshark/SKILL.md) | Review saved DNS/authentication captures with query/reply, protocol-tree and frame context. |
| [wpscan](skills/wpscan/SKILL.md) | Scope WordPress plugin/user inventory and distinguish detection, account access and incomplete vulnerability evidence. |
| [wrapwrap](skills/wrapwrap/SKILL.md) | Generate PHP resource-wrapper chains and validate envelope, byte transformations and consumer limits. |
| [xargs](skills/xargs/SKILL.md) | Run explicit item lists with literal boundaries, finite concurrency and child-status evidence. |
| [xclip](skills/xclip/SKILL.md) | Transfer exact local bytes to/from a chosen X11 selection and verify owner/session/clipboard lifetime. |
| [xfreerdp](skills/xfreerdp/SKILL.md) | Open an approved RDP desktop with version-aware FreeRDP options and verify remote identity and session outcome. |
| [xml-pp](skills/xml-pp/SKILL.md) | Format trusted XML while retaining original bytes, parse failures and entity-handling limits. |
| [xxd](skills/xxd/SKILL.md) | Inspect, render plain hex and reconstruct exact bytes; distinguish offsets, columns, patching and text encoding. |
| [ysoserial](skills/ysoserial/SKILL.md) | Generate selected Java serialization fixtures without confusing producer failures, binary output and target effects. |
| [yubisim](skills/yubisim/SKILL.md) | Generate an authorized Yubico OTP while preserving token counters and distinguishing output from validator acceptance. |
| [zbarimg](skills/zbarimg/SKILL.md) | Decode local QR/barcode images and distinguish decoded content, image errors and incomplete multi-image results. |
| [zenmap](skills/zenmap/SKILL.md) | Open saved scan results and distinguish GUI profiles, selected rows and actual Nmap command/completion evidence. |
| [zip](skills/zip/SKILL.md) | Package selected source/data trees with deliberate recursion, exclusions, Unix symlink handling and member/integrity checks. |
| [zipalign](skills/zipalign/SKILL.md) | Check or align an owned APK with native-library page requirements and the correct signing order. |

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
