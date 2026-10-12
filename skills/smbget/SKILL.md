---
name: smbget
description: Retrieve a selected SMB file or approved directory subtree with Samba smbget. Use when identity, guest mode, domain defaults, recursive flags or partial-transfer evidence affects a download.
---

# Retrieve one SMB file

Read this entire SKILL.md before acting; reuse complete current context. Require the authorized URL, intended known account/domain and fresh private local destination. For an approved directory subtree, read [recursive retrieval](references/recursive-retrieval.md) fully before that procedure. Otherwise use the single-file task below. Check installed options, perform the selected transfer and finish with its status, remote path and local content evidence or the concrete failure.

Use Samba's `smbget --version` and `smbget --help`. Historical releases used different short switches: current Samba uses `--workgroup` (`-W`) and `--recursive`, while `-R` selects name resolution. Choose supported long options rather than copying an old `-w ... -R` command.

Define `domain` and `user` as the intended identity, `url` as the exact `smb://server/share/path/file` and `output` as a fresh absolute file path. Quote the whole URL, especially literal dollar signs and spaces. Under a trusted Samba configuration and the intended authentication environment:

~~~bash
umask 077
test ! -e "$output" || exit 1
smbget --workgroup="$domain" --user="$user" --outputfile="$output" "$url"
status=$?
~~~

Enter the password at the prompt; do not put it in the URL or `%PASSWORD` argument. Existing password environment variables, credentials/cache and client configuration can affect authentication, so resolve unexpected prompt/domain behavior before retrying. A displayed default workgroup is not the requested AD domain. If SMB encryption is required, select the installed client's supported encryption policy; a successful ordinary transfer alone does not prove encryption.

Require zero status and the expected file, retain byte count and a locally computed digest, and compare expected content/version where available. A progress total is not an integrity comparison. Keep a failed partial file separate from a completed artifact.

Share discovery or a read label does not prove access to this file. Permission denied can also reflect a malformed URL or a directory passed as a file: verify object type, path and authentication context before concluding the ACL denied access. Do not turn one failure into attempts against multiple accounts.

The single-file command deliberately omits `--recursive`, `--resume` and `--update`. Those change scope or reuse local data; `--outputfile` is incompatible with recursion and stdout mode. A timestamp-based update skip is not proof of identical bytes. Consult the installed version's [Samba manual](https://www.samba.org/samba/docs/current/man-html/smbget.1.html) for these choices.
