---
name: smbclient
description: List SMB shares and retrieve selected files with Samba smbclient. Use to distinguish share discovery from read access and to choose anonymous, password or Kerberos authentication on Linux.
---

# Samba smbclient

Read this entire SKILL.md before acting. Select the intended server/share and explicit authentication context, distinguish discovery from the requested file operation, and preserve its result. Kerberos, bulk retrieval and replacement below are conditional tasks; finish with identity/share/path, transfer status and content evidence or a concrete access/coverage gap.

This is Samba's `smbclient`, not Impacket's differently shaped SMB shell. Check `smbclient --version`. Define `server` as the target hostname/IP. An explicit empty-user, empty-password share-list attempt is:

~~~bash
smbclient -L "$server" -U '%' -N
~~~

`-N` alone only suppresses the password prompt; it does not select an empty username. A share listing does not establish access to its contents. A trailing `SMB1 disabled -- no workgroup available` message can follow a successful share listing; assess that output before changing protocols.

Define `share` from the listing and `domain`/`user` for the chosen known identity. Open the share interactively and enter the password at the prompt:

~~~bash
smbclient "//$server/$share" -U "$domain/$user"
~~~

For an anonymous connection, replace `-U "$domain/$user"` with `-U '%' -N`. For an explicitly intended guest account with an empty password, use `-U "$domain/guest%" -N`. These are different requests. Omitting `-U` can select a local environment/cache identity, and a prior NetExec login is not inherited. A server may also map a request to guest; successful listing alone does not prove which identity it granted. Inside the SMB prompt, use `ls`, `cd` and `get` for selected remote files; `lcd` sets their local destination. Quote names containing spaces. Record the remote share/path alongside downloaded files.

For a deliberately selected subtree, `recurse ON`, `prompt OFF` and `mget *` enable bulk retrieval. Set a fresh local directory and narrow the remote directory first. These session settings persist; `mget *` at the share root can copy much more than intended. A denied directory/file is a partial result, even when other downloads succeed.

For metadata on one selected file, use `allinfo "name with spaces.txt"` at the SMB prompt, replacing the illustrative name. Retain the returned stream names/sizes and diagnostics. A zero-byte default `::$DATA` stream does not establish that every named stream is empty. The returned `altname` is an alternate 8.3 filename, not an alternate data stream. Ordinary file retrieval does not establish preservation of all stream metadata; report exactly which object was inspected or copied.

For an existing Kerberos file cache, define `cache` as its absolute path and `server` as the service's correct DNS name. On versions supporting these switches:

~~~bash
smbclient "//$server/$share" --use-krb5-ccache="FILE:$cache" -N
~~~

That option requires Kerberos rather than silently falling back. Use `-I "$server_ip"` if an explicit connection address is needed while retaining the service hostname. Check cache identity/expiry and name resolution before treating authentication failure as an incorrect password. Do not infer write access from successful reads.

Share-level access labels do not settle a particular file's permissions. Read, create, overwrite and delete are distinct operations. For a requested file replacement, preserve its content and relevant metadata first; `del` followed by `put` leaves a gap and can change metadata, so it is not an atomic update. A successful upload of a logon script proves transfer, not execution or the identity of a future process. Keep the exact account, share, path and observed operation with the result.

Quoting discipline on the Linux side decides credential results: a password containing `!` passed inside double quotes (for example copied from a hint with `\!` escaping) yields a literal backslash in the password and a `NT_STATUS_LOGON_FAILURE` that mimics wrong credentials. Use single quotes around `domain/user%password` so history/escape handling cannot alter the value. A share-permission table from another tool (a `READ`-only row for SYSVOL/NETLOGON) reflects that tool's root-open probe, not file-level create/write ACLs; settle writability by uploading and deleting one probe file with `put`/`del` in the target directory before concluding. When planting a modified logon script, poll the consuming account's SAMR `queryuser` fields (`Logon Time`, `logon_count`, `bad_password_count`) to detect the periodic interactive logon that executes it — a network-type logon (WinRM) never runs `scriptPath`-style scripts, so a rising `logon_count` with no script execution indicates the wrong logon type.

Resolve identity defaults and authentication switches against the installed version of the [Samba smbclient manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html).
