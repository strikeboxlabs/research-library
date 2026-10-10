# Export selected Grafana verifier records

Work from a coherent acquired database copy. Confirm it is SQLite; an HTTP 200/login page saved as `grafana.db` is not an acquisition. Preserve source/version, row identity and sidecar limitations. A table named `user` alone does not establish Grafana or the password algorithm.

Define `database` as the existing absolute working-copy path. Inspect the actual schema, then a bounded set of identities and storage metadata:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail "$database" 'PRAGMA table_info("user");'
sqlite3 -init /dev/null -readonly -batch -bail -header -column "$database" \
  'SELECT id,login,typeof(password) AS verifier_type,length(password) AS verifier_chars,typeof(salt) AS salt_type,length(CAST(salt AS BLOB)) AS salt_bytes FROM "user" ORDER BY id LIMIT 20;'
~~~

These commands assume the displayed historical column names after inspection. If the schema differs, adapt the query; absent columns are not an empty credential set. External-auth accounts may lack a useful local password verifier. Grafana `is_admin` is application authority, not Linux root. A login/email is a service-account association, not proof of an identically named OS account.

For the one selected numeric `id`, define `query` as `SELECT id,login,password,salt,rands FROM "user" WHERE id = ...;` with the reviewed literal ID, and `records` as a new private CSV path:

~~~bash
umask 077
(set -o noclobber; sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" "$query" >"$records")
~~~

Require query success and exactly the intended row; failure can leave a partial export. Keep the CSV header/quoting and parse it with a CSV reader. Do not flatten a display row into colon-separated values or join fields from different accounts. `password` contains a verifier in the supported historical version; `salt` is its literal salt string. `rands` is a separate field: the 8.0.0 password derivation takes password and salt, not `rands`. Do not hex-decode a salt merely because it resembles hexadecimal text.

For Grafana 8.0.0, upstream `EncodePassword` derives **50 bytes of PBKDF2-HMAC-SHA256 with 10,000 iterations**, then stores hexadecimal. Other versions/backends need their own verified producer rules. Export the complete original verifier and retain its row mapping before conversion. A 100-character hex value supports a byte-length observation, not algorithm identification by itself. Finish with selected rows, verified parameters and acquisition limits, without placing the private records in a general report.

See [8.0.0 password derivation](https://github.com/grafana/grafana/blob/v8.0.0/pkg/util/encoding.go), [SQLite CLI modes](https://sqlite.org/cli.html) and [WAL acquisition constraints](https://sqlite.org/wal.html).
