---
name: impacket-smbclient
description: Browse SMB shares and transfer selected files with Impacket's Linux SMB client, including Kerberos-cache authentication. Use when Impacket smbclient is installed or Samba command syntax does not apply.
---

# Select the share, then verify the transfer

Read this entire file before acting. Identify the server, authentication context, share and local destination. Finish with the selected paths, transfer result and useful file evidence; successful SMB login does not establish access to every share.

Check `impacket-smbclient -h`. Set `server` to the real server name and `identity` to `domain.example/user`. With a matching `KRB5CCNAME` cache:

~~~bash
impacket-smbclient -k -no-pass "$identity@$server"
~~~

For password authentication, omit `-k -no-pass` and the password from the target string to use the prompt. `-no-pass` is not a request for privileged or anonymous access. Kerberos requires the proper server identity, realm and time; replacing the hostname with an IP can select the wrong service principal.

In the client console, use the installed `help` output. The following paths are illustrative and must be replaced:

~~~text
shares
use Documents
cd Reports
ls *
lcd /absolute/private/output
get selected-report.pdf
exit
~~~

`lcd` changes the local destination and `cd` changes the remote location. Choose a destination without a conflicting filename, then verify the saved file's size/format and hash if a trusted expected hash exists. A directory listing is not proof of file-read permission; a partial local file after failure is not a completed download.

For a requested upload, select the exact remote directory and use `put LOCAL_FILE`, then verify the remote entry and, when required, retrieve it to compare bytes. Upload, overwrite, deletion and ACL changes are real writes; share enumeration should not silently include them. `get` selects one file; `mget` and especially recursive `rget` can widen collection substantially.

An access-denied response after connecting concerns the selected share/path or operation. Path-not-found can indicate the wrong share root, path separators or a DFS referral. Current builds can expose `dfs_info` and `dfs_mode`; following a referral contacts another endpoint, so inspect it before expanding the connection scope. Console `shell` runs locally, not on the SMB server. See [Impacket's console implementation](https://github.com/fortra/impacket/blob/master/impacket/examples/smbclient.py) for the actual command grammar.
