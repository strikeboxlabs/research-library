# Read a bounded account-SID mapping

Require one owned server/domain, a known login pair, permission for the account catalogue query and an explicit small RID-prefix budget. NetExec's `--rid-brute` name describes repeated SID lookups, not password guesses, but it still performs authenticated RPC requests. A share listing alone does not establish that RPC policy allows the query.

Reuse `nxc_bin`, `target`, `domain`, `users_file` and `passwords_file` as the entrypoint's single known pair. Define `rid_limit` as the approved positive upper bound and `report` as a fresh private transcript. In the reviewed implementation the query starts at zero and covers RIDs below this bound in batches; it is not a selectable starting RID:

~~~bash
umask 077
"$nxc_bin" smb "$target" -d "$domain" -u "$users_file" -p "$passwords_file" \
  --no-bruteforce --rid-brute "$rid_limit" > "$report" 2>&1
status=$?
~~~

Inspect RPC connection/policy diagnostics and coverage before interpreting an empty result. Preserve RID, returned domain, name and SID type. A member server's account-domain SID can differ from a DC's directory domain; do not prepend a guessed domain SID to every returned name. Missing mappings within a completed prefix differ from unqueried higher RIDs or an interrupted/denied request.

CLI formatting and SID-type labels vary by release. A grep on `TypeUser` followed by a fixed whitespace field is not a stable record parser or proof that every result is a human account; machine/service accounts can also be represented in the account catalogue. Retain the original mapping and resolve object class separately when needed. Returned names establish neither enabled logon, passwords, group membership nor protocol access, and are not an automatic authentication-attempt list. See the [SMB RID query implementation](https://github.com/Pennyw0rth/NetExec/blob/main/nxc/protocols/smb.py).
