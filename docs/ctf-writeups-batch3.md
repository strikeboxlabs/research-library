# Third CTF writeup batch

Reviewed 2026-10-09. All ten supplied Hack The Box writeups were processed: 180 physical PDF pages were text-extracted and read, with 51 selected pages rendered and visually inspected. The batch adds 21 independent tool skills and enriches 10 existing ones, bringing the catalogue to 51.

Each new skill is one `SKILL.md`, about 277–357 words including metadata and sources. The existing secretsdump package gains one optional reference for the distinct offline NTDS workflow. There is no shared runtime layer, mandatory source companion or dependency on another tool's skill. Raw PDFs, screenshots, source snapshots and extracted text stay in ignored `ingest/` and `work/pdf-ingest-batch3/`.

## Coverage of all ten documents

Pages below are one-based physical PDF pages, including covers. Repeated commands were reviewed without adding duplicate prose when existing skills already handled them.

| Document | Pages | Guidance accepted from this source |
|---|---:|---|
| `AI.pdf` | 12 | Festival text2wave fixtures and safe text input (5–8); jdb attachment, deferred breakpoints, suspended frames and expression execution (10–11). |
| `Alert.pdf` | 14 | ffuf path/extension/vhost comparison (3–5); HTTP callback and encoded evidence interpretation (6–11); Hashcat APR1 mode (11); pspy scheduled-process observation (13). |
| `Altered.pdf` | 19 | Wfuzz paired-input truncation, leading-zero coverage and session state (7–9); MySQL server file reads/writes and ambiguous HTTP failures (11–17); script PTY behavior (18). |
| `Ambassador.pdf` | 16 | SearchSploit candidate review (4); curl literal paths and response evidence (5–7); Git history without checkout changes (11–13); Consul KV ACLs, combined configuration and reload effects (13–16). |
| `Analysis.pdf` | 37 | ffuf filter combinations (4); Wfuzz parameter-name discovery (7); literal LDAP filter escaping and invalid-versus-empty results (8–10). BloodHound partial collection/NTLM fallback (17) and replication/credential distinctions (36–37) confirm existing guidance. |
| `Analytics.pdf` | 9 | curl evidence instead of version-string grep (3); explicit Python server directory/binding and actual shell interpreter (5); environment/container observations inform interpretation limits (7–8). |
| `Antique.pdf` | 10 | UDP follow-up coverage and SNMP subtree/type handling (3–5); Chisel reverse forwarding (8). Historical CUPS behavior was reviewed but not generalized to current installations. |
| `Anubis.pdf` | 18 | John NetNTLMv2 input (10); Chisel/ProxyChains direction and TCP limitations (8–9); OpenSSL CSR/certificate distinction (7, 16), clean PEM conversion and MIT PKINIT configuration (16–17). |
| `Appsanity.pdf` | 28 | Temporary HTTP/SMB transfers (9, 14–17); Chisel reverse listener mapping and Ncat service interaction (15, 27); GNU strings adaptation of the Windows triage workflow (22). GUI decompilation/disassembly was reviewed as context. |
| `APT.pdf` | 17 | RPC interface binding versus active calls (3–5); IPv6 coverage (5–6); ZIP conversion and offline NTDS (7); Kerbrute user inventory, SSH IPv6 destinations and login-failure limits (8–9); remote registry context and service lifecycle (10–11). |

New skills: `chisel`, `consul`, `curl`, `ffuf`, `git`, `impacket-reg`, `impacket-rpcmap`, `impacket-smbserver`, `jdb`, `kerbrute`, `kinit`, `ncat`, `openssl`, `proxychains`, `pspy`, `python-http-server`, `script`, `searchsploit`, `snmpwalk`, `strings`, `text2wave`.

Enriched skills: `bash`, `hashcat`, `impacket-secretsdump`, `john`, `ldapsearch`, `mysql`, `netexec`, `nmap`, `ssh`, `wfuzz`. Earlier deferrals for curl, Ncat and terminal handling are now addressed in these specific supported workflows; this does not claim complete coverage of those utilities.

## Corrections and decisions

- **Java and speech:** synthesizing a WAV does not establish how a recognizer transcribes it. Text is passed through a file/stdin, not interpolated into `os.system` shell code. jdb expression method calls execute in the JVM, and a deferred or initialization breakpoint is not proof that a request will stop there.
- **HTTP discovery:** byte/word/line filters require measured negatives. ffuf combines filters with OR by default. A protected `401`/`403` site can be a useful result. Host-header changes alone do not select HTTPS SNI. No system-wide hosts-file edits are needed by the accepted curl example.
- **Paired payloads:** Altered's zip iterator runs only 254 pairs when its second list has 254 entries; that is not a complete run through the first list. Its initial range also omits leading-zero four-digit strings. Rate-limit evasion is not built into the reusable comparison procedure.
- **Database writes:** `LOAD_FILE` reads on the database server and has privilege/path/size restrictions; successful reading does not prove directory write permission. `INTO OUTFILE` writes a new server file. Altered demonstrates why HTTP 500 does not prove that a side effect failed.
- **History and Consul:** inspect old blobs with `git show` instead of changing the checkout. A discovered old token is not proof of present validity. `consul kv put test ...` writes real state and is not an authentication-only probe; read, write and agent-reload rights are separate. Script checks execute under the agent's OS identity.
- **SNMP:** Antique's displayed `BITS` value includes both hex bytes and set-bit annotations. Decoding every displayed token as hex creates spurious suffix data. Net-SNMP source confirms the formatter behavior; the skill explains a selected-value re-query. A default MIB-2 walk misses enterprise branches. UDP follow-up must retain `-sU`, which one printed pipeline omits.
- **Tunnel boundaries:** reverse Chisel destinations are reached from the client, while their listeners are on the server. Explicit loopback/high-port listeners avoid accidental exposure and privileged local ports. ProxyChains carries compatible TCP calls, not raw/UDP traffic; MIT's TCP preference still permits fallback. A connected tunnel is not proof of destination service access.
- **Certificates:** `openssl req -verify` verifies a CSR signature, not CA trust or issued identity. Clean PEM conversion is separate from textual inspection. The accepted MIT setting is `pkinit_identities`; the writeup misspells it. PKINIT uses the issued certificate/key and verified trust inputs.
- **Offline evidence and authentication:** ZIP conversion preserves complete records and separates stderr; NTDS requires matching SYSTEM data, not an unnecessary SECURITY hive for this operation. `-just-dc-user` is rejected in LOCAL mode. Historical credentials may be stale. Switching to Kerberos does not grant unlimited password attempts; [Microsoft documents Kerberos retries counting toward account lockout](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/account-lockout-threshold).
- **RPC and registry:** rpcmap can fall back to many UUID bind probes; `-brute-opnums` invokes methods, and maximum 5 means six operations, 0–5. A bind or non-fault reply needs protocol-specific interpretation. Impacket reg may start/change RemoteRegistry even for `query` and attempts restoration; a registry query is not necessarily operationally read-only. HKU is not automatically every account's complete hive.
- **Runtime interpretation:** strings/GUI analysis give leads, not proof a DLL loaded or a path executed. A pspy UID observation does not establish file writability. A container-like hostname or `.dockerenv` file alone does not identify the host's credentials or patch state. `sh script` does not honor a Bash shebang as an interpreter override.

Tool-specific primary manuals/source are linked inside each package. Rolling upstream behavior was checked during authoring; installed help and actual Linux behavior still need verification. Windows examples adapted to Linux (GNU strings and Ncat) are identified as adaptations, not claimed literal replays.

## Reviewed material not turned into skills

| Candidate | Remaining work or reason for omission |
|---|---|
| Burp browser workflows, SQL/LDAP injection scripts, XSS/session chains | Application-specific procedures, not independently supported CLI utilities. Preserve their generic request/filter/evidence lessons in accepted skills. A repeatable application fixture is needed for a separate methodology. |
| Visual Studio, WinDbg, dnSpy and Ghidra GUI paths | Analysis and Appsanity contain substantial Windows/GUI reverse engineering. A Linux CLI adaptation such as headless Ghidra or ilspycmd needs its own documented workflow and fixture; a GUI screenshot is insufficient. |
| Metasploit/msfvenom, Responder, NTLM relay and impacket-psexec | Dedicated skills still need coherent configuration, side-effect/cleanup and failure guidance. The supplied payload/handler, poisoning, service-creation and downgrade chains were reviewed, not copied into generic recipes. No external cracking service was used. |
| CUPS ErrorLog disclosure, kernel exploits, OverlayFS/unshare chains | Historical configuration/version-specific exploit demonstrations. Kernel version strings alone do not establish distribution patch status. Need exact builds, prerequisites and disposable reproductions before generalizing. |
| AD certificate-template/account changes | Need original-state capture and reliable restoration after partial failure. Existing-certificate inspection/authentication is covered; template modification is not. |
| sqlite3, base64, printenv, uname, gcc, file, basic copy/archive commands | No separate skill added just because a command appears. Generic use is already expected; encoding, provenance and interpreter pitfalls were folded into relevant procedures. |

All ten documents are processed; these omissions are explicit scope decisions, not unread files. Source credentials, flags, target addresses and one-off payloads were not copied into reusable skills.

## Source fingerprints

SHA-256 identifies the exact input even if the ignored inbox is replaced by the next batch.

| File | SHA-256 |
|---|---|
| AI.pdf | `4e309a51cf7bc29fd6a733202d613869b3555a3072f92b50c95d6d155e5dde4e` |
| Alert.pdf | `0b775d3cc8aa9ce61b5414cf5c3c7f62af7c502dd9eab8ed9e1d671a205dda22` |
| Altered.pdf | `e690bddec853a09beab978d16f227b8f667fdcfb4278f904750a685a85ecc301` |
| Ambassador.pdf | `ad3acb627c3c500df37f7fadcd505d74ca03cf5104712863877feebd37334d94` |
| Analysis.pdf | `4d841d1e4dd10f8fec59872cebad887cf47766552ad7ce13a6a616886e640169` |
| Analytics.pdf | `eb65250fa5c0740f216e2892d3460c8062d8c97ed04f3b064ac9a642be2d8b4e` |
| Antique.pdf | `33eea35803ec3a84aa7b87dafb22e23bbefea348ecfe634a5d7fe1a9087e18a3` |
| Anubis.pdf | `2d6961098639d9a8448e8c0e57c2ac5c4debffe85a2b6682c6de246f636f804f` |
| Appsanity.pdf | `62ed65fc1958cf4b5986734b92141a9da64c7d81b56f297dcc4c3b4b904893e2` |
| APT.pdf | `9007726d4c0d362991fca91f56fdad7e7256153a78266169af89f069e1adee16` |

See the [validation record](validation.md) for checks actually executed. The [Linux getting-started guide](../GETTING_STARTED.md#2-adapt-to-this-machine) remains the next step for local binary/help adaptation and success/failure fixtures. Documentation and packaging review do not establish improved worker performance.
