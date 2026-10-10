# Use an available PostgreSQL extension when psql is missing

A containerized database does not determine whether the client shell has `psql` or PHP's `pgsql` extension. Check the selected PHP CLI independently. A socket at port 5432 is a lead, not proof of a database identity or successful authentication.

For an authorized connection, use an existing reviewed libpq service entry with explicit host, port, database, role and applicable TLS settings. Supply its name through `PGSERVICE`; keep the password in the existing protected libpq password file, not source code. Save this reviewed snippet as a local CLI file outside any served web directory:

~~~php
<?php
if (!extension_loaded('pgsql')) {
    fwrite(STDERR, "This PHP CLI lacks pgsql.\n");
    exit(1);
}
if (!getenv('PGSERVICE')) {
    fwrite(STDERR, "Select the intended libpq service first.\n");
    exit(1);
}
$db = pg_connect('connect_timeout=5');
if ($db === false) {
    fwrite(STDERR, "PostgreSQL connection failed.\n");
    exit(1);
}
$result = pg_query($db, 'SELECT current_database() AS db, current_user AS role');
if ($result === false || ($row = pg_fetch_assoc($result)) === false) {
    fwrite(STDERR, "Database identity query did not return its row.\n");
    pg_close($db);
    exit(1);
}
printf("database=%s role=%s\n", $row['db'], $row['role']);
pg_close($db);
~~~

Define `service` as that entry's name and `script` as this file; set `php_bin` to the selected PHP CLI, lint the file and then run:

~~~bash
"$php_bin" -l "$script"
PGSERVICE="$service" "$php_bin" -f "$script"
~~~

An **illustrative** result `database=profiles role=report_reader` establishes the connected database and SQL role, not the OS user or permission to read every table. A missing extension, connection rejection and failed SQL statement are different failures. Preserve the associated diagnostic privately and check that layer before changing credentials or queries. `localhost` refers to the executing process's network context; a host and container can reach different services.

For a later authorized data query, request only relevant columns/rows and use `pg_query_params` for variable values. A successful zero-row result is different from `pg_query` returning `false`; do not treat either as a recovered credential. A value's encoding-like appearance alone is not a reason to transform it.

See [PHP connection handling](https://www.php.net/manual/en/function.pg-connect.php), [query results](https://www.php.net/manual/en/function.pg-query.php), [parameter binding](https://www.php.net/manual/en/function.pg-query-params.php), [libpq service entries](https://www.postgresql.org/docs/current/libpq-pgservice.html) and [password files](https://www.postgresql.org/docs/current/libpq-pgpass.html).
