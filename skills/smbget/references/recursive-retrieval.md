# Retrieve the approved directory subtree

Require one approved directory URL including its server/share/path, the known account/domain and a fresh empty private `capture_dir`. Establish the byte/time scope before recursion; this traverses descendants, with no depth or maximum-file-size bound in this recipe. Narrow to selected files instead if the whole subtree is unnecessary.

Check installed help as in the entrypoint. Define `directory_url`, `domain`, `user` and fresh absolute `transfer_log` outside the capture directory:

~~~bash
umask 077
(cd "$capture_dir" && smbget --recursive --workgroup="$domain" --user="$user" "$directory_url") \
  > "$transfer_log" 2>&1
status=$?
~~~

Enter the known password at the prompt; log redirection can change prompt visibility, so use the installed client's approved credential mechanism if unavailable. This omits resume/update/outputfile and starts from empty local state. A printed workgroup/account is not independent proof of remote session identity. For an intended guest transfer, replace account options with supported `--guest`; do not mix guest and explicit account flags.

Check status, log, resulting paths/sizes and expected inventory. A downloaded total with denied children can leave partial coverage. Existing local files, timestamp skips and changing remote contents are not an atomic backup or digest match. Retain partial artifacts separately on failure and compare known digests before parsing/executing acquired content. See [Samba recursion and guest options](https://www.samba.org/samba/docs/current/man-html/smbget.1.html); old -R recursion differs from current name-resolution -R.
