---
name: netexec
description: Validate known SMB credentials, interpret share checks, read selected user metadata and inspect LDAP machine-account quota with NetExec on selected lab hosts. Use to avoid unintended credential combinations and distinguish authentication, password status, privilege indicators and path permissions.
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

`STATUS_PASSWORD_MUST_CHANGE` and `STATUS_PASSWORD_EXPIRED` are distinct account/password states, not generic bad-password results. Preserve the exact status. Changing a known password is a separate state-changing operation; do not treat the status as permission to reset accounts or continue guessing.

For selected share enumeration, inspect this version's `--shares` implementation. The reviewed current code checks write access by opening the share root with requested access masks; `--file-write-check` instead creates/deletes a probe directory/file and may leave artifacts after failure. Older versions can differ. A share-level READ/WRITE result does not establish permission to read, replace or delete a particular nested file; preserve path-level evidence separately.

Old NTDS records may contain stale credentials. A generic logon failure can also reflect domain selection, account restrictions or authentication policy. Keep the original failure and distinguish those causes before retrying. Switching to Kerberos is not an unlimited-attempt workaround: failed Kerberos authentication can count toward account lockout. Preserve the same account/request budget across protocols.


# Read selected user metadata

If this release supports `smb --users USER`, define `requested_user` as one known account name in the target's account domain. Reuse the single known login pair above:

~~~bash
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" --no-bruteforce --users "$requested_user"
~~~

Current [SAMR handling](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb/samruser.py) resolves that name before querying its details; omitting the name enumerates users. Record the returned account domain: a member server's local SAM and a DC's AD domain are different contexts. A missing row or RPC error is not an empty description or proof the account does not exist.

The description is administrator-supplied text; a password-like string there is an exposure finding, not evidence of a current valid credential. Preserve only the needed redacted evidence. `BadPW`/historical `badpwdcount` is not a remaining-attempt allowance. AD's [badPwdCount](https://learn.microsoft.com/en-us/windows/win32/adschema/a-badpwdcount) is maintained per DC without replication and can reset after successful authentication; zero does not establish a clean domain-wide history. Keep DC/time with the observation and use effective account policy separately when evaluating lockout risk.

# Read the domain machine-account quota

When the question concerns domain join policy, inspect `ldap --help` and this installation's `maq` module. Reuse the single known pair above, with `target` set to the selected domain controller:

~~~bash
"$nxc_bin" ldap "$target" -d "$domain" -u "$users_file" -p "$passwords_file" --no-bruteforce -M maq
~~~

The module reads `ms-DS-MachineAccountQuota`; it does not create a computer. An illustrative `MachineAccountQuota: 10` is a domain policy value, not ten accounts still available to this user. Existing quota usage, domain join rights and permissions on the intended container need separate evidence. Zero does not negate explicitly delegated computer-creation rights. An empty LDAP result or failed bind is unknown, not zero; preserve the error and domain/DC before deciding whether another query is warranted.

A disabled `SeMachineAccountPrivilege` in one process token does not settle directory creation rights. Conversely, a positive quota does not establish permission to change another object's delegation settings or impersonate users. See the [module implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/modules/maq.py) and [domain join permission rules](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/active-directory-domain-join-permissions) for these separate conditions.
