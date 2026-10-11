---
name: sqlmap
description: Test one authorized HTTP parameter from a captured request and inspect selected database metadata or rows. Use when request fidelity, stale sessions, heuristic findings or excessive extraction make SQL injection evidence ambiguous.
---

# Preserve the request and scope the test

Read this entire SKILL.md before acting. Require the selected endpoint's authorization for the actual test and any metadata/row retrieval, a complete current request and the bounded settings below. No conditional resources are required. Finish with confirmed versus heuristic findings and retrieval coverage; missing authentication, unstable responses or an interrupted run remain unresolved.

Check `sqlmap --version` and `sqlmap -hh`, including support for `--time-limit` and `--disable-hashing`. This procedure actively changes HTTP parameters and sends repeated requests; choose an endpoint approved for that testing. Risk level 1 is not a guarantee against application side effects.

Define `request` as a private raw HTTP request file containing the method/path, Host, required headers, blank line and body. Confirm its ordinary response and current authentication before testing. Define `parameter` as the observed parameter to test, `seconds` as the approved positive per-invocation time budget and `case_dir` as a new private output directory for this target/session. In Bash:

~~~bash
umask 077
sqlmap_args=( -r "$request" -p "$parameter" --level=1 --risk=1
  --threads=1 --timeout=10 --retries=1 --time-limit="$seconds"
  --output-dir="$case_dir" )
sqlmap "${sqlmap_args[@]}"
~~~

For HTTPS, establish the intended scheme explicitly; add `--force-ssl` when the raw request does not supply enough information. Resolve cookies, anti-CSRF tokens, redirects and login-page responses before attributing differences to injection. Read interactive choices; `--batch` selects default answers and does not itself constrain testing or extraction. Broader test levels, techniques or parameters need a deliberate scope change.

Distinguish a heuristic suggestion from a reported injectable parameter and identified technique. Retain the parameter, request context, DBMS evidence and relevant confirmation output. A negative result covers these settings and this session only. Rate limits, timeouts, unstable responses or an expired session leave the result incomplete. A database version banner does not establish the web application's exact version.

## Discover only the metadata needed

Once the finding supports the task, define `database` as the selected database name and list its accessible tables:

~~~bash
sqlmap "${sqlmap_args[@]}" -D "$database" --tables
~~~

Choose `table` from that result, then inspect its columns:

~~~bash
sqlmap "${sqlmap_args[@]}" -D "$database" -T "$table" --columns
~~~

Do not copy an application-specific table name from a walkthrough. Empty or denied results can reflect the database account's visibility or retrieval failure. Enumerating every database with `--dbs` is a broader step, useful only when the database identity is actually missing and that scope is intended.

For PostgreSQL, sqlmap's database abstraction uses **schemas**: a reported current “database” such as `public` can be the current schema, not the connected PostgreSQL database name. Preserve the tool's label and distinguish schema/table namespaces from server databases in the finding; check the installed version's [metadata query definitions](https://github.com/sqlmapproject/sqlmap/blob/master/data/xml/queries.xml) when this distinction matters. A database-superuser result is authority in that database service, not UID zero on its operating system. Query capability and OS-command execution remain separate results; metadata alone cannot complete an execution claim.

If an authorized data sample is needed, define `columns` as the comma-separated observed field names needed for the finding, preferably non-sensitive proof fields:

~~~bash
sqlmap "${sqlmap_args[@]}" -D "$database" -T "$table" -C "$columns" \
  --dump --start=1 --stop=1 --disable-hashing
~~~

The row range bounds requested rows, not the HTTP request count or a stable transactional snapshot. `--disable-hashing` disables hash analysis of dumped values. Keep output/session files private and verify whether retrieval completed; a timed-out or truncated value is partial evidence.

Sqlmap can reuse stored injection information and query results. Keep the same case directory for this investigation, but use a fresh one when changing targets or materially changing the baseline. `--fresh-queries` bypasses cached query results; it does not reset every saved finding. Preserve earlier evidence before considering any session deletion.

Consult the [sqlmap usage guide](https://github.com/sqlmapproject/sqlmap/wiki/Usage) for request, detection and retrieval controls, and the [CLI definitions](https://github.com/sqlmapproject/sqlmap/blob/master/lib/parse/cmdline.py) when installed options differ.
