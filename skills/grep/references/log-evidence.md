# Search readable logs and interpret misplaced values

Use this when the current process can read relevant application/system logs or an acquired log tree. Select a bounded directory from the observed service and preserve original files. Membership in Debian-style `adm` often permits reading many logs, but actual ownership, modes, ACLs and namespace determine access; it does not grant every log or general administrator authority.

Define `log_dir` as the selected directory and `matches`/`errors` as fresh private output files. An initial search can combine literal route/field clues without dumping unrelated logs:

~~~bash
umask 077
LC_ALL=C grep -rnF -e 'password' -e 'reset_password' -- "$log_dir" \
  >"$matches" 2>"$errors"
status=$?
~~~

The patterns are alternatives, not an AND condition. `-n` retains line numbers and recursive results normally retain filenames. Current GNU `-r` follows command-line symlinks but skips links found during descent; `-R` follows all of them and can expand the selected scope. Choose that deliberately rather than inheriting it from a walkthrough. Inspect status and errors even when matches exist: denied/disappearing files leave coverage incomplete. A result of 1 means no match in what was searched; 2 indicates an error. Binary/compressed rotations need the appropriate acquired-format reader, not a blanket assertion that grep examined their decoded records. Log rotation can change files while searching.

Use the matching file and line to inspect a small surrounding context. Define `log_file`, an observed `line_no`, and fresh private `context`/`context_errors` files:

~~~bash
start=$((line_no > 2 ? line_no - 2 : 1))
end=$((line_no + 2))
sed -n "${start},${end}p" "$log_file" >"$context" 2>"$context_errors"
~~~

Keep the source filename, timestamp, request method/route and exact field relationship. Neighboring lines may be other clients, not the same session; correlate request IDs, account references and time only when the format supports that association. Preserve raw bytes privately and redact unrelated secrets from ordinary reports.

An **illustrative** request fragment `POST /reset_password?email=EXAMPLE_CANDIDATE` with status `500` establishes that the query value reached this logged request. It does not establish that it is a password, that it belongs to the account being examined or that the reset succeeded. A value inconsistent with the expected email/username shape can be a misplaced credential hypothesis, but could also be arbitrary test input. Apache's ordinary request-line logging can retain query values; a POST method does not imply the value was confined to an unlogged body. A 500 also does not establish rollback.

Distinguish URL percent/form decoding from Apache's log escaping; don't blindly replace every escape before preserving the original record. Treat account names from `/etc/passwd` or another directory as OS-account leads, not proof of the log value's owner or of an application's separate user database.

If the current task permits a selected credential-reuse test, choose the evidenced account/service and submit that one candidate using the appropriate prompt/client. For an existing local OS account, `su --login "$account"` uses the local authentication policy; run `id` in the resulting session to establish its actual identity. An application or Splunk account with the same name is a separate authentication decision. A denial can reflect policy, expiration, terminal requirements or a wrong candidate; retain its diagnostic and revisit the evidence rather than starting an unrequested broad guessing loop. No candidate needs to be pre-proven valid before a scoped test, and success in one service does not prove reuse elsewhere.

Finish with the selected search scope, unreadable/undecoded material, relevant record/context and candidate status (hypothesis, tested acceptance or unresolved). A password-looking match alone is not a successful lateral-movement result.

Primary references: [GNU recursive file selection](https://www.gnu.org/s/grep/manual/html_node/File-and-Directory-Selection.html), [grep exit-status caveats](https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html), [Apache request/query logging and escaping](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html), [Debian group meanings](https://sources.debian.org/src/base-passwd/3.5.51/doc/users-and-groups.sgml), [util-linux su](https://github.com/util-linux/util-linux/blob/master/login-utils/su.1.adoc).
