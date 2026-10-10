# Selected application authentication rows

Start with the entrypoint's coherent read-only database copy and actual table schema. A Rails `development.sqlite3` filename is a lead, not proof this is the database currently used by the service. A consistent snapshot/WAL set and configuration/source association matter before treating its records as current.

For a schema actually exposing `users(id, username, password_digest, role, ...)`, define `database` as the acquired copy:

~~~bash
sqlite3 -init /dev/null -readonly -batch -bail "$database" '.schema users'
sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" 'SELECT id, username, role, typeof(password_digest) AS storage_type, length(password_digest) AS stored_length FROM users ORDER BY id LIMIT 20;'
~~~

This bounded metadata view keeps role/account/storage facts together before selecting sensitive records. Confirm the columns in this database; do not transplant the query to another schema without adapting it. A record absent from this snapshot differs from a query/schema failure. Role labels such as administrator are application authority, not OS group membership or UID.

For a selected numeric row identifier, retain its complete verifier and identity mapping in a private structured export. The following uses an **illustrative selected id 2**; substitute the confirmed required identifier:

~~~bash
umask 077
sqlite3 -init /dev/null -readonly -batch -bail -header -csv "$database" 'SELECT id, username, role, password_digest FROM users WHERE id = 2 LIMIT 1;' >"$records"
~~~

Define records as a fresh private CSV file. Check query status and parse CSV properly; default pipe-separated `SELECT *` loses explicit column association and can be ambiguous. Preserve the original full verifier without rewrapping, stripping its prefix or assuming a fixed cost from the field name. An observed complete `$2a$12$...` record is a bcrypt-family candidate with its embedded revision/cost; verify the consumer and installed offline loader instead of treating every Rails record as identical.

When an offline check is authorized, transfer the actual full verifier into that loader's supported record format and keep the row/account association separately. A bcrypt record normally does not require a special Rails converter. Converter banners, CSV header fields and abbreviated screenshot strings are not part of the hash. A failure to load an incomplete record cannot be solved by more candidate passwords.

A recovered application candidate is a reuse hypothesis for another service or OS account. A real-name field or similar username can help choose a single authorized account check, but does not establish identity equivalence. Record the selected service's own authentication/identity result separately; application role, database row, Unix passwd entry and current process groups are distinct evidence. Avoid copying unnecessary other user records to support one selected check.

References: [SQLite CLI schema/CSV](https://www.sqlite.org/cli.html), [read-only WAL conditions](https://www.sqlite.org/wal.html#read_only_databases) and [John's bcrypt loader](https://github.com/openwall/john/blob/bleeding-jumbo/src/BF_fmt.c).
