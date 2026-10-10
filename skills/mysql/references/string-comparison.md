# Investigate string truncation and comparison

At the SQL prompt, replace `observed_table` with the selected real table:

~~~sql
SELECT VERSION(), @@SESSION.sql_mode;
SHOW FULL COLUMNS FROM `observed_table`;
SHOW CREATE TABLE `observed_table`;
~~~

Read the type, character limit, collation and actual unique constraints. Frontend length checks and a shortened display do not establish the database schema. The CLI session's SQL mode may differ from the application's connection.

- `VARCHAR` retains trailing spaces within its limit; `CHAR` normally strips them on retrieval. Retrieval and equality comparison are separate questions.
- For nonbinary strings, `PAD SPACE` collations ignore trailing spaces in equality comparisons; `NO PAD` collations preserve their significance. On MySQL versions providing it, inspect the actual collation's `INFORMATION_SCHEMA.COLLATIONS.PAD_ATTRIBUTE`. Do not infer this solely from a case-insensitive suffix or the connection default.
- Overlength nonspace input can be truncated with warnings in non-strict mode; strict mode normally rejects it, while `IGNORE` can downgrade errors. Excess trailing spaces have separate rules: `VARCHAR` truncates them with a warning, `CHAR` silently, regardless of strict mode.

For a statement already executed in your session, run `SHOW WARNINGS` immediately, before another nondiagnostic statement replaces its diagnostics. It cannot retrieve warnings from an earlier web request's session. Establish the schema, application query and connection settings before attributing an identity collision to truncation; avoid inserting probe accounts or relaxing SQL mode just to explain an observation.

Consult the server version's [string-type rules](https://dev.mysql.com/doc/refman/8.4/en/char.html), [SQL modes](https://dev.mysql.com/doc/refman/8.4/en/sql-mode.html) and [warning scope](https://dev.mysql.com/doc/refman/8.4/en/show-warnings.html) for exceptions. MariaDB and older MySQL releases require their own matching documentation.
