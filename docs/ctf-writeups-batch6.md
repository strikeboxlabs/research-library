# Sixth CTF writeup batch

Reviewed 2026-10-09. All five supplied Hack The Box writeups were processed: **73 physical PDF pages** were text-extracted and read, with **29 selected pages** rendered and visually inspected. This batch adds **nine independent tool skills** and enriches **nine existing skills**, bringing the catalogue to **87**.

Each new package contains one `SKILL.md`. Curl gains one conditional reference for API requests. Workers need only selected skill folders; the intake record is maintenance documentation, not a runtime dependency. Originals and intermediate evidence remain in ignored `ingest/` and `work/pdf-ingest-batch6/`.

## Coverage of all five documents

Page numbers are one-based physical PDF pages, including covers. Repeated commands were reviewed without adding duplicate guidance.

| Document | Pages | Accepted guidance |
|---|---:|---|
| `Baby.pdf` | 10 | LDAP identity/attribute coverage (3–5); exact password-state interpretation and a known-account password change (5); SAM versus NTDS identity and extraction versus cracking (6–10). |
| `BabyTwo.pdf` | 11 | Share labels versus file-specific permissions, upload versus execution and replacement effects (2–8); pyGPOAbuse defaults, client scope, partial writes and incomplete cleanup (9–11). |
| `Backdoor.pdf` | 15 | Stopped jobs, process arguments and process evidence (8–12); gdbserver transport/modes (9–11); find predicates and command-display quoting (12–14); Screen ownership, multiuser conditions and session lifecycle (12–15). |
| `Backend.pdf` | 18 | Method-specific API discovery and JSON versus form requests (2–10); process-relative procfs reads (12–13); exact JSON text extraction, body construction and local JWT handling (14–16); log matches as candidate evidence (18). |
| `BackendTwo.pdf` | 19 | API validation, authentication and stale token claims (3–10, 13–15); unpadded base64url, JSON file handling and process environment interpretation (10–16); PAM stack requirements, scoped file searches and text-filter constraints (17–19). |

New skills: `find`, `gdbserver`, `grep`, `jq`, `jwt-tool`, `ps`, `pygpoabuse`, `screen`, `smbpasswd`.

Enriched skills: `base64`, `curl`, `ffuf`, `gobuster`, `impacket-secretsdump`, `ldapsearch`, `netexec`, `smbclient`, `sudo`.

## Corrections and useful distinctions

- **Identity and password state:** Baby's broader LDAP output does not prove that an entry missing from username-only output is a non-user object. Search filters, returned attributes and access affect visibility. Inspect the observed DN and attributes. `STATUS_PASSWORD_MUST_CHANGE` differs from `STATUS_PASSWORD_EXPIRED`; the shown utility is `smbpasswd`, not the prose's `smbpassword`. Changing a known credential is a persistent operation, distinct from an administrative reset. SAM and NTDS records do not become the same identity because account names/RIDs match. Decrypting stored hashes is not cracking plaintext passwords; the failed login alone does not establish its cause.
- **Share checks and file effects:** BabyTwo's share-level READ result does not establish the permissions of every file. Its successful delete/upload proves those particular operations in that context. Delete followed by upload is not atomic and can affect metadata. A transferred logon script is not proof of execution or future process identity. Current NetExec source distinguishes access-mask checks from the optional file-write probe; older examples must be checked against the installed implementation.
- **GPO defaults and restoration:** selecting a GPO GUID does not confine its effects to the connection's DC. Current pyGPOAbuse can default to creating an administrator account when no nonempty command is supplied, and defaults its task modification date into the past. The accepted fixture uses an explicit harmless marker command and truthful date. Target-name options need filtering enabled, whose effective XML/client scope still needs validation. Writes span SYSVOL XML, LDAP attributes/versions and `gpt.ini`; failures can leave partial state. The reviewed cleanup path deletes the entire task XML and does not restore prior attributes/versions, despite its help text. A captured before-state and restoration method are necessary for a controlled mutation.
- **Process and debugger interpretation:** Backdoor describes Ctrl-Z as backgrounding; the shown job is stopped. NUL-separated argument memory is not a string with mysteriously missing spaces. A process listing need not preserve original shell quoting. `/proc/cmdline` is the kernel boot line; the Backend command actually reads `/proc/self/cmdline`, which refers to the server-side reader. Environment values are leads, not proof of current working directory or exact imported module. An exposed gdbserver gives process-control access by design; the evidence does not establish a specific GDB 9.2 vulnerability. The documented TCP host component is ignored, so writing a loopback address is not sufficient binding protection. The new skill uses an SSH/stdio fixture and distinguishes remote from extended-remote mode.
- **Find and Screen:** `find -empty` can recurse and match regular files unless depth/type are constrained. It is not an atomic synchronization mechanism. Suppressing stderr can conceal incomplete searches. A session named `root` does not prove its current shell identity. Cross-user Screen attachment depends on build, privileges and ACLs; the lab's success is not universal access to privileged sessions. Setting TERM does not allocate a terminal. Detaching, sharing, taking over and terminating a session have different effects.
- **API methods and formats:** a route discovered with GET may behave differently under POST; even an empty POST can mutate state. Filtering every `405` can hide valid routes, and FastAPI `422` can be an input-validation clue. Backend's prose mixes `/user` with `/users`, `v1` with `vi`, signup with login and bearer tokens with cookies. Its later curl request is described as POST although the shown invocation selects GET. Use the actual request and application schema. Signup JSON, login form data, a documentation page and its schema fetch are distinct requests. An account-role change need not rewrite an issued JWT.
- **Bytes, JSON and tokens:** `jq -r` appends a newline, while a missing field can quietly produce `null`. The accepted extraction checks record count/type and uses `-j` for text without an added newline. JSON strings are Unicode text, not arbitrary binary transport. A serializer handles quotes, backslashes and newlines more reliably than BackendTwo's replacement chain. Its base64url helper uses unquoted input and wrapping-prone encoding; the accepted form uses quoted printf, GNU no-wrap mode and explicit alphabet translation. Unpadded base64url, ordinary base64 and URL percent encoding are different. JWT decoding does not verify a signature; application settings establish the real signing key and permitted algorithm. Ticarpi's tool must be distinguished from similarly named packages and its signing options from verification modes.
- **Authentication and text filtering:** BackendTwo's additional PAM challenge is separate from the ordinary password. A required-module failure may be reported after other prompts; this differs from sudo policy denial. Grep's multiple patterns are alternatives, not a requirement to match all. The shown word-list filters omit positional/repeated-letter constraints, so their candidates are not a complete solution to the game. Password-looking strings in failed-login logs remain leads without identity/validity evidence.

Primary manuals and implementations are linked inside each accepted package. The changes are documentation-reviewed; current-source semantics do not establish compatibility with historical packages or successful Linux execution.

## Reviewed material not turned into skills

| Material | Decision and remaining work |
|---|---|
| Baby's DiskShadow/Robocopy backup acquisition and persistent shadow-copy steps | Native Windows operations remain context for the existing offline NTDS skill. A snapshot is not automatically an independent complete copy. Any reusable acquisition procedure needs matching artifacts, VSS lifecycle and cleanup evidence in a Windows-specific package. No broad credential collection or password spray was added. |
| BabyTwo's hosts-file command, PowerView ACL/password writes and logon-script callback | The shown `tee /etc/hosts` overwrites rather than appends; it was not copied. Home-directory names remain candidate identities. The native Windows chain and callback payload are not general Linux utility skills. A future procedure must preserve exact directory/file state and affected-client scope. The Linux pyGPOAbuse tool received its own independently researched, bounded skill. |
| Backdoor's custom LFI PID loop, shellcode and Metasploit handler | The displayed Python loop lacks request timeouts and uses brittle response replacement. It was not promoted into a generic collector. Retained process and debugger semantics instead. No complete exploit or generic Metasploit skill was inferred from a handler excerpt; transport exposure is described without assuming an unverified version-specific vulnerability. |
| Backend/BackendTwo's application-specific password reset, mass assignment and application-file backdoor | Retained request encoding, token-state and file-reconstruction lessons. Persistent application/account changes and stealth/backdoor payloads were not made default CLI workflows. Reproducing the application behavior requires a separate fixture, observed authorization/state model and restoration path. |
| BackendTwo's custom PAM game and application-specific word solver | Retained PAM diagnostics and the limits of grep candidate filtering. The game does not justify a general authentication-bypass procedure or a dedicated module skill. |
| Repeated Nmap, BloodHound, Evil-WinRM, strings, PTY, transfer and ordinary shell commands | Existing skills already cover the demonstrated decisions. The appearance of a utility alone did not justify another skill or more prose. GUI activity and native Windows commands remain source context. |

All five PDFs are processed; these are deliberate coverage decisions, not unread documents. Unrelated assessment methodologies and pre-existing uncommitted work were preserved.

## Source fingerprints

SHA-256 identifies the exact originals even after the ignored inbox is replaced.

| File | SHA-256 |
|---|---|
| Baby.pdf | `09b15554fe4b97aafe065f8e418a4216ca7f80ef8c87b440d5c69db992b611cf` |
| BabyTwo.pdf | `5b5316c2c00b044e225fe08851837922b35966f551aeac739b480b7b81650ad7` |
| Backdoor.pdf | `a22b7c8e9dcb9ea22699eb152e14695f69571b875d42adb2ca382ce628b9bfe7` |
| Backend.pdf | `53b9fa290f207eeaca9bbdf37e4410682d1ce6b0ccdb724f23cefe50a21ad7f2` |
| BackendTwo.pdf | `19394a993bcc5f98e279603b9592ab90f3c841b1c399d1364d62853c942a2b68` |

See the [validation record](validation.md) for checks actually executed. The [Linux adaptation guide](../GETTING_STARTED.md#2-adapt-to-this-machine) describes installed-help checks and meaningful success/failure fixtures on the intended host.
