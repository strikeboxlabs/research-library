---
name: rpcclient
description: Query Windows/Samba RPC identities and perform a selected authorized SAMR password reset from Linux. Use to resolve names/RIDs, inspect user/group evidence and distinguish authentication, RPC rights and account-change results.
---

# Resolve the object through the intended RPC service

Read this entire file before acting. For account changes read [SAMR password changes](references/samr-password-changes.md) fully. Finish with the server/domain, resolved object and RPC result; successful login does not establish rights for every RPC method.

Check `rpcclient --help`. Set `server` to the selected hostname and `identity` to `DOMAIN/user`; omit the password from argv to use the prompt:

~~~bash
rpcclient -U "$identity" "$server"
~~~

Within the console, start with the required lookup rather than broad enumeration:

~~~text
help
lsaquery
lookupnames selected-user
queryuser 0x451
queryusergroups 0x451
~~~

The username and RID are illustrative: use the actual lookup result. A RID belongs to a particular SAM domain SID; the same number on another machine/domain identifies a different principal. `queryusergroups` reports memberships returned by that interface, not the complete current access token or a universal effective-permissions calculation. `querygroupmem` can resolve a selected group's members. `enumdomusers` is useful when domain enumeration itself is in scope.

For a repeatable read, `-c 'lsaquery'` supplies a command without an interactive session. Multiple semicolon-separated commands are parsed by rpcclient, so do not concatenate untrusted account names into that string. `-N` suppresses a password prompt; it does not grant anonymous access or convert supplied credentials into a valid session.

| Failure | Interpretation/next check |
|---|---|
| `NT_STATUS_LOGON_FAILURE` | Verify identity/domain and the permitted authentication method before retrying credentials. |
| Access denied after connecting | The selected RPC operation can require rights not implied by SMB authentication. |
| Name not found or no such user | Recheck server/domain and the exact object identifier. |
| Unsupported method/information class | Check installed/server implementation and method help; do not reinterpret it as lack of an object. |

Use the [Samba manual](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) and interactive `help COMMAND` for available operations. If Kerberos is required, use the installed Samba credential-cache/required-Kerberos options with the correct server name; an IP-only identity can select the wrong SPN path.
