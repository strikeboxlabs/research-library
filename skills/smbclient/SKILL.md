---
name: smbclient
description: List SMB shares and retrieve selected files with Samba smbclient. Use to distinguish share discovery from read access and to choose anonymous, password or Kerberos authentication on Linux.
---

# Samba smbclient

This is Samba's `smbclient`, not Impacket's differently shaped SMB shell. Check `smbclient --version`. Define `server` as the target hostname/IP. An explicit empty-user, empty-password share-list attempt is:

~~~bash
smbclient -L "$server" -U '%' -N
~~~

`-N` alone only suppresses the password prompt; it does not select an empty username. A share listing does not establish access to its contents. A trailing `SMB1 disabled -- no workgroup available` message can follow a successful share listing; assess that output before changing protocols.

Define `share` from the listing and `domain`/`user` for the chosen known identity. Open the share interactively and enter the password at the prompt:

~~~bash
smbclient "//$server/$share" -U "$domain/$user"
~~~

For an anonymous connection, replace `-U "$domain/$user"` with `-U '%' -N`. Inside the SMB prompt, use `ls`, `cd` and `get` for selected remote files; `lcd` sets their local destination. Quote names containing spaces. Record the remote share/path alongside downloaded files.

For a deliberately selected subtree, `recurse ON`, `prompt OFF` and `mget *` enable bulk retrieval. Set a fresh local directory and narrow the remote directory first. These session settings persist; `mget *` at the share root can copy much more than intended. A denied directory/file is a partial result, even when other downloads succeed.

For an existing Kerberos file cache, define `cache` as its absolute path and `server` as the service's correct DNS name. On versions supporting these switches:

~~~bash
smbclient "//$server/$share" --use-krb5-ccache="FILE:$cache" -N
~~~

That option requires Kerberos rather than silently falling back. Use `-I "$server_ip"` if an explicit connection address is needed while retaining the service hostname. Check cache identity/expiry and name resolution before treating authentication failure as an incorrect password. Do not infer write access from successful reads.

Documentation reviewed 2026-10-09; Linux execution untested. Case: Active PDF pp. 3–6. Maintenance source: [Samba smbclient manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html).
