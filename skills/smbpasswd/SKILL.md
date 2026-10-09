---
name: smbpasswd
description: Change one known account's SMB password with Samba smbpasswd from Linux. Use when a required password change blocks login and the remote server, account identity and mutation scope are established.
---

# Distinguish password change from a login test

Confirm Samba's `smbpasswd` and its local help. `STATUS_PASSWORD_MUST_CHANGE` means the account requires a password change before logon; it is distinct from `STATUS_PASSWORD_EXPIRED` and a generic authentication failure. Preserve the exact response. Do not collapse it into a wrong-password result or retry many candidates.

A password change is a persistent account operation, not harmless validation. Use this workflow when changing the named account is part of the task and the current credential is known. An administrator resetting another account's password is a different operation with different permissions and consequences.

Run as an ordinary local user. Define `server` as the intended writable SMB/domain password endpoint, `domain` as the verified account domain and `account` as the exact account name:

~~~bash
smbpasswd -r "$server" -U "$domain/$account"
~~~

Enter the old password and the selected new password twice at the prompts. Without `-r`, the default target is local; under root, smbpasswd also supports direct local account-database administration. Do not add `sudo`, `-a`, `-x` or `-n` to repair a remote change failure. Those options can add, delete or clear local SMB account credentials rather than solve the remote operation.

Keep passwords out of `user%password` command arguments and shared transcripts. The new password must meet the server's policy and the account must be allowed to change it. Password history/minimum age, a disabled/locked account, wrong domain, unavailable endpoint and unsupported protocol are different failure causes. An old manual's NT-domain PDC wording is not a reason to guess the current AD endpoint or downgrade SMB globally.

After a reported change, verify once through the intended authentication path within the task's attempt budget. A successful password change does not grant WinRM or administrative access. On a timeout or ambiguous response, determine the actual account state before another mutation; do not assume it rolled back. Record account, endpoint, time and outcome without retaining passwords in the report. Existing sessions and other clients may still use the old credential.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Baby p. 5. Sources: [Samba smbpasswd](https://www.samba.org/samba/docs/current/man-html/smbpasswd.8.html), [status definitions](https://github.com/fortra/impacket/blob/master/impacket/nt_errors.py).
