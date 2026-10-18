---
name: kerbrute
description: Check a bounded list of candidate AD usernames against a selected KDC with Kerbrute userenum. Use when old account inventories need validation without switching to password guessing.
---

# Kerbrute username checks

Read this entire SKILL.md before acting. Require the selected KDC/domain, small reviewed candidate list and request budget. No conditional resources are required. Finish with actual tested counts, result categories and untested/error cases; missing scope or endpoint information prevents this task, rather than justifying discovery against other servers.

Inspect `kerbrute version` and `kerbrute userenum --help`. This skill covers `userenum`; `passwordspray`, `bruteuser` and `bruteforce` perform different authentication attempts and are not automatic follow-ups.

Define `domain` as the full domain/realm, `dc` as the intended reachable KDC, `users_file` as a small deduplicated list of candidate usernames, and `log` as a fresh private output file:

~~~bash
umask 077
kerbrute userenum -d "$domain" --dc "$dc" --delay 500 --safe -v -o "$log" "$users_file"
~~~

The delay is milliseconds and makes the reviewed implementation use one thread. Verify local support and choose a request budget appropriate to the list. `--safe` stops when a locked account is reported; it is not proof that an operation is silent or harmless. Avoid the encryption-downgrade switch for routine inventory.

`userenum` constructs Kerberos AS requests without guessing passwords. KDC responses can distinguish unknown principals from accounts requiring preauthentication. This is network authentication-protocol activity and can be logged or monitored. Some accounts can return AS-REP material; protect logs accordingly rather than treating them as an ordinary public username list.

When deriving names from an old directory dump, preserve domain/account mapping and distinguish users, machine accounts and disabled or deleted historical entries. A successful name check does not prove a usable password, enabled interactive logon, SMB access or WinRM permission. Do not turn a large stale dump into an unbounded password/hash attempt list.

Distinguish the three response classes before counting hits: unknown principal (`KDC_ERR_C_PRINCIPAL_UNKNOWN`), valid user (`KDC_ERR_PREAUTH_REQUIRED`), and known-but-disabled/revoked (`KDC_ERR_CLIENT_REVOKED` — krbtgt and Guest commonly return this on a DC). `CLIENT_REVOKED` proves the name exists; do not merge it into the invalid bucket. Sanity-check the run by including `krbtgt` in the list: if it does not come back revoked/valid, the response mapping or list handling is broken. `userenum` sends no pre-auth timestamp, so its results stay valid even when the KDC clock is skewed hours off; only password-based AS exchanges break on skew.

Inspect verbose failures and the final tested count. Timeout, realm mismatch, clock/network errors or early cancellation can leave candidates untested; absence from the success list is not always proof the account does not exist. Specify the KDC explicitly when DNS discovery could select a different server. Report the checked list, endpoint, result categories and incomplete cases without adding password guesses.

Sources: [upstream modes and options](https://github.com/ropnop/kerbrute), [userenum implementation](https://github.com/ropnop/kerbrute/blob/master/cmd/userenum.go).
