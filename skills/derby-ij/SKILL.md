---
name: derby-ij
description: Inspect an existing Apache Derby database copy using the ij SQL CLI. Use when embedded JDBC paths, schema selection, truncated output, driver compatibility or database locks block a bounded inspection.
---

# Inspect a Derby working copy with ij

Use a consistent copy acquired while the database was shut down, or through Derby's supported online backup procedure. An ordinary archive of a live database may mix incompatible states. Preserve the acquisition and inspect a separate writable working copy: even a read-only SQL connection can require database boot/recovery and filesystem writes. Embedded Derby opens local files; Derby also supports network-server operation, so an absent listening port is not a universal product property.

Launch the installed `ij` from a trusted Derby distribution with its matching libraries and compatible JDK. Its startup banner identifies the version. A missing JDBC driver or unsupported Java class version calls for checking the launcher/classpath/JDK, not modifying the database or switching the system-wide Java default.

At the `ij>` prompt, replace the example absolute path with the existing working-copy directory. SQL and ij commands end in semicolons:

~~~sql
connect 'jdbc:derby:/absolute/path/to/working-copy/ofbiz';
readonly on;
show connections;
show schemas;
show tables in OFBIZ;
describe OFBIZ.USER_LOGIN;
select USER_LOGIN_ID from OFBIZ.USER_LOGIN
  order by USER_LOGIN_ID fetch first 5 rows only;
disconnect;
exit;
~~~

Use `OFBIZ`, `USER_LOGIN` and the selected column only if schema discovery confirms them; they illustrate one application's layout. A successful connect selects a connection; `SHOW CONNECTIONS` marks the current one with `*`. `READONLY ON` restricts SQL data changes on that connection, not every filesystem effect. Do not add `;create=true` to fix an incorrect path or `;upgrade=true` during inspection.

**Illustrative result decisions:** a schema listing containing `OFBIZ` supports qualifying table names with it. A bounded SELECT returning five rows establishes only that those rows were visible. Zero rows, a missing table and a failed connection are different outcomes. Check the current connection/schema and identifier case before concluding the acquisition lacks application data. For case-sensitive names, use ij's documented quoted-string form with `DESCRIBE`, and SQL delimited identifiers in queries.

Select only relevant columns and use a specific predicate for detailed inspection. If displayed text ends with a truncation marker, increase `maximumdisplaywidth`, for example `maximumdisplaywidth 512;`, and repeat that bounded query. Confirm the width covers the whole field before copying a structured record; a partial digest is not usable input for another tool. NULL is not an empty string.

If the database is already booted by another embedded process, do not delete lock files or open the application's active directory. Return to the consistent working-copy boundary. An incompatible database format, encryption/authentication requirement or recovery error needs its own resolution; creating a new database would conceal the failure.

Use the [connection reference](https://db.apache.org/derby/docs/10.13/tools/rtoolsijcomref22318.html), [ij metadata commands](https://db.apache.org/derby/docs/10.4/tools/rtoolsijcomrefshow.html) and [backup guidance](https://db.apache.org/derby/docs/10.9/adminguide/cadminbckupdb.html) for version-specific recovery.
