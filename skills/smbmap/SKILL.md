---
name: smbmap
description: Enumerate SMB share access and retrieve selected files with SMBMap. Use when default write probes, recursive flags, guest mapping or automatic downloads could change the meaning or scope of an inventory.
---

# Enumerate without a write-permission probe

Read this entire SKILL.md before acting. Select inventory or requested file recovery, identify the endpoint/account and keep the selected operation bounded. Finish with session identity, actual access or transfer evidence and incomplete coverage; missing implementation options or credentials are prerequisites to resolve.

Inspect `smbmap --help` for the installed generation. Current upstream uses `-r` with `--depth`; older writeups use `-R`. Do not translate recursive flags by name alone.

**The default share permission check can create and delete test directories/files.** For a listing that does not test write access, keep `--no-write-check`. Define `host`, `domain` and `username` for one intended endpoint and known account:

~~~bash
smbmap -H "$host" -d "$domain" -u "$username" --prompt --no-write-check
~~~

Enter its password at the prompt. A session mapped to Guest is not authentication as the supplied username. Capture the reported session identity and distinguish successful connection, share visibility and actual access. Omitting write checks means write permission remains untested, regardless of how a summary labels the share.

Define `share_path` as one observed share or share-relative directory. Bound directory traversal using installed help:

~~~bash
smbmap -H "$host" -d "$domain" -u "$username" --prompt --no-write-check -r "$share_path" --depth 1
~~~

Permission-denied children limit coverage; root-level READ does not establish access to every file. `-A` is an automatic regex-matched **download** option requiring traversal, not merely a display filter. Avoid adding it to an inventory command. `--no-update` suppresses progress messages; it is not the switch that prevents remote writes. Administrative checks and remote execution are separate modes.

For one requested file, define `remote_file` in the installed command's SMB path syntax, such as `share\directory\file`, and work from a dedicated private local directory:

~~~bash
smbmap -H "$host" -d "$domain" -u "$username" --prompt --no-write-check --download "$remote_file"
~~~

Read the reported destination instead of assuming the remote basename became a local filename. Confirm transfer status, local size and expected format before parsing; partial downloads and blocked reads are not empty files. If a prior write probe reports failed cleanup, retain the exact reported object path and handle that specific residue rather than issuing broad deletes.

See [upstream usage](https://github.com/ShawnDEvans/smbmap) and the [argument and permission-check implementation](https://github.com/ShawnDEvans/smbmap/blob/master/smbmap/smbmap.py) for installed-generation differences.
