---
name: netexec
description: Validate known SMB credentials with NetExec on selected lab hosts. Use to avoid unintended user/password combinations and distinguish authentication, local admin indicators and access to other protocols.
---

# NetExec credential checks

Check the installed entrypoint (`nxc` or `netexec`), version and `smb --help`. Historical `crackmapexec` examples are not a version guarantee. This procedure checks a known credential on one selected host; it does not select execution or credential-dumping modules.

Define `nxc_bin` as the verified executable, `target` as one in-scope host, `domain` as the intended AD domain, and `users_file`/`passwords_file` as private absolute files containing exactly one corresponding username/password each. Check both exist: otherwise a filename can be treated as a literal credential. File paths avoid exposing the password in the command line, but NetExec's output/database can still retain credentials.

~~~bash
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" --no-bruteforce
~~~

For a local account, select the supported `--local-auth` mode instead of the domain option. Establish the intended identity before retrying a failure.

When multiple known pairs are explicitly in scope, retain one-to-one line order, equal counts and no accidental blank lines. Without `--no-bruteforce`, separate username/password lists generally produce every combination. The reviewed implementation repeats a single password across multiple users even with pairing mode: that is still multiple login attempts. Pairing is not a lockout safeguard.

By default a successful authentication can stop further attempts for that host. Therefore a success does not mean every supplied pair was checked. Use `--continue-on-success` only when completing the approved pair inventory is intended. Observe failure/lockout status and the agreed attempt budget; do not turn failures into automatic spraying.

Record host, protocol, domain/account, status and which checks actually ran. A positive SMB login does not prove read access to every share, WinRM access or remote execution. The admin indicator reflects NetExec's protocol-specific privilege check. Errors/timeouts and stopped runs leave coverage incomplete; never interpret an empty result as universal credential invalidity.

Old NTDS records may contain stale credentials. A generic logon failure can also reflect domain selection, account restrictions or authentication policy. Keep the original failure and distinguish those causes before retrying. Switching to Kerberos is not an unlimited-attempt workaround: failed Kerberos authentication can count toward account lockout. Preserve the same account/request budget across protocols.

Documentation reviewed 2026-10-09; Linux execution untested. Cases: Administrator p. 8; APT pp. 8–9. Sources: [credential CLI](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/cli.py), [pairing and stop behaviour](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/connection.py), [SMB options](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb/proto_args.py), [account lockout and Kerberos retries](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/account-lockout-threshold).
