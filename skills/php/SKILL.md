---
name: php
description: Inspect PHP CLI configuration and run controlled checks, including PostgreSQL connection diagnosis through the pgsql extension. Use for CLI/web SAPI differences, missing extensions, PHAR behavior or misleading image headers.
---

# PHP CLI reproduction context

Define `php_bin` as the intended executable, which may be a versioned binary rather than the default `php`:

~~~bash
"$php_bin" -v
"$php_bin" --ini
"$php_bin" -m
"$php_bin" -r 'echo PHP_VERSION, " ", PHP_SAPI, PHP_EOL;'
~~~

Record the binary, SAPI, loaded configuration and relevant extensions. CLI results do not establish the version/configuration used by Apache or FPM. An HTTP version header is a separate observation; testing local PHP 8.2 does not reproduce a service merely reporting 8.3.2. `-n` ignores ini files and may omit extensions, so use it only when that configuration difference is intentional.

For an existing reviewed source file, define `script` and lint it before any intended execution:

~~~bash
"$php_bin" -l "$script"
~~~

Lint checks syntax, not application behavior, runtime dependencies, reachable classes or security. Normal PHP startup/configuration still matters. To execute a small reviewed snippet, `-r` accepts PHP code without `<?php` tags; keep shell quoting intact and pass variable input as arguments rather than interpolating it into PHP source. Running a supplied script or calling `unserialize` is code execution, not merely inspection of an artifact.

`-d name=value` changes configuration for that invocation, subject to the directive's rules. For PHAR creation, `phar.readonly` controls whether PHP archives can be written; some changes are constrained by the startup ini. Reading an archive does not require a blanket machine-wide setting change. Keep any creation-specific override on the controlled CLI invocation and use a fresh output path.

For PHAR behavior, match the version and API actually called. PHP 8.0 stopped automatically unserializing PHAR metadata on ordinary archive loading; explicit metadata access is a different operation. A failed older demonstration therefore does not alone establish a patched application, harmless metadata or a missing gadget.

`getimagesize` can accept a non-image and return nonsensical dimensions. A `GIF89a` prefix plus reported dimensions is not proof of a valid decodable image or a pure image file. Use the intended image decoder and retain the original bytes. When wrappers or application transformations change a response, verify exact lengths and contents; do not invent missing bytes to make a parser accept it.


## Use an available PostgreSQL extension when psql is missing

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

Define `service` as that entry's name and `script` as this file; lint with the earlier command, then run:

~~~bash
PGSERVICE="$service" "$php_bin" -f "$script"
~~~

An **illustrative** result `database=profiles role=report_reader` establishes the connected database and SQL role, not the OS user or permission to read every table. A missing extension, connection rejection and failed SQL statement are different failures. Preserve the associated diagnostic privately and check that layer before changing credentials or queries. `localhost` refers to the executing process's network context; a host and container can reach different services.

For a later authorized data query, request only relevant columns/rows and use `pg_query_params` for variable values. A successful zero-row result is different from `pg_query` returning `false`; do not treat either as a recovered credential. A value's encoding-like appearance alone is not a reason to transform it.

See [PHP connection handling](https://www.php.net/manual/en/function.pg-connect.php), [query results](https://www.php.net/manual/en/function.pg-query.php), [parameter binding](https://www.php.net/manual/en/function.pg-query-params.php), [libpq service entries](https://www.postgresql.org/docs/current/libpq-pgservice.html) and [password files](https://www.postgresql.org/docs/current/libpq-pgpass.html).
