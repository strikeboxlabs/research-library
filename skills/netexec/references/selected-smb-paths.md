# Select one SMB path or ordinary file

Require one owned host, a known login pair and explicit share/folder scope. Reuse the verified `nxc_bin`, `target`, `domain` and one-line `users_file`/`passwords_file` from the entrypoint. Inspect this installation's `smb --help` for these options. Define `share`, `folder` and `depth` as the approved share, relative folder and finite recursion bound, and `pattern` as a literal filename substring:

~~~bash
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" \
  --no-bruteforce --spider "$share" --spider-folder "$folder" \
  --depth "$depth" --pattern "$pattern"
~~~

This searches metadata without `--content`; matching names do not prove readable bytes. A narrow pattern limits reported matches, not necessarily folders traversed. `--regex` is a different matching mode; `.` broadly matches names. Keep the selected root/depth and traversal errors with results. See [spider options](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb/proto_args.py) and [traversal implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb/smbspider.py) when interpreting version-specific depth behavior. Denied paths or filtered names leave coverage incomplete.

For one approved ordinary document, define `remote_file` as its exact share-relative path with literal backslashes and `local_file` as a fresh absolute private destination. This is independent authorization from listing metadata:

~~~bash
umask 077
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" \
  --no-bruteforce --share "$share" --get-file "$remote_file" "$local_file"
~~~

Set the share explicitly: the reviewed default is `C$`. Single-quote a literal path containing spaces/backslashes when defining the variable; do not copy doubled Python-display escapes as extra separators.

The [transfer implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb.py) opens/truncates the local destination before attempting the download and can retry with read/write access after a failed read-only open. A failed attempt may therefore leave an empty or partial file. Preserve its diagnostic and avoid treating local existence alone as success. Require the success receipt, plausible byte count, expected format and a recorded local SHA-256; compare an authoritative remote checksum when available. Encrypted-document recognition is distinct from opening its content. Keep acquired bytes private and do not execute them.

Finish with host/identity, share-relative source, destination, byte/hash receipt and unresolved transfer or traversal failures. See [file operation syntax](https://www.netexec.wiki/smb-protocol/get-and-put-files) for installed-version reconciliation.
