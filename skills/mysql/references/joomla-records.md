# Joomla database context and selected password records

Use for authorized Joomla database inspection with an acquired active `configuration.php` or equivalent application configuration. Read the PHP source as text; importing/including it is unnecessary code execution. Preserve the actual `JConfig` properties `dbtype`, `host`, `user`, `password`, `db` and `dbprefix`. A stale backup can differ from the running service; don't guess a default prefix or treat the database account as an application administrator.

Choose the actual driver/endpoint before connecting. Joomla `mysqli` indicates MySQL-compatible access. Unix `localhost` can select a socket; remote `127.0.0.1` means the application's host, not the workstation. A local listener on 3306 is a classic-protocol lead; 33060 is commonly X Protocol and is not interchangeable with the mysql CLI endpoint. A port number alone does not identify a server. Define `db_host`, `db_port`, `db_user`, `database` from the selected classic TCP endpoint:

~~~bash
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database"
~~~

For an intended local Unix socket, use its verified socket path with `--protocol=SOCKET --socket=...` instead. Prompt for the known password; keep required TLS and account-matching rules. A denied login, wrong protocol, missing socket and refused TCP listener are separate failures. A PTY may help an interactive interface, but mysql's batch operation does not inherently require an interactive Bash or script session.

At the SQL prompt:

~~~sql
SELECT USER(), CURRENT_USER(), DATABASE(), VERSION();
SHOW TABLES;
~~~

Confirm the observed prefix and actual users table. Joomla schema notation `#__users` is a placeholder replaced by the configured prefix, not necessarily a literal table. For the **illustrative** observed prefix `site_`, inspect columns and a selected account:

~~~sql
SHOW COLUMNS FROM `site_users`;
SELECT id, username, password, block
FROM `site_users`
WHERE username = 'reviewed-account'
ORDER BY id
LIMIT 2;
~~~

Substitute actual identifiers and SQL-quoted account literals. Two rows, no rows and a denied SELECT need different next checks; use the selected unique ID for export. Preserve username/ID association and `block` state; the row does not itself establish OS or application role/group membership. A blanket `SELECT *` collects unrelated email/registration/parameter data and makes copied rows easy to misinterpret.

To export the selected verifier, define `query` as a reviewed one-row `SELECT password FROM <actual users table> WHERE id = <selected ID> LIMIT 1`, and `record_file` as a fresh private file:

~~~bash
umask 077
mysql --protocol=TCP --host="$db_host" --port="$db_port" --user="$db_user" --password --database="$database" \
  --batch --skip-column-names --execute="$query" > "$record_file"
status=$?
~~~

Require a successful status and the expected single complete record. Batch output escapes special characters; an ordinary bcrypt alphabet needs no such unescaping, but don't generalize to arbitrary formats. Keep ID/account mapping separately from the verifier input. SQL output headers, PDF line wraps, labels and surrounding quotes are not part of the record.

Joomla 4.2.6's default user helper selects bcrypt, but acquired databases may contain older/migrated formats. A complete `$2y$10$...` record is 60 characters including variant, cost, salt/checksum; retain all fields. HashID's bcrypt candidate and Hashcat mode 3200 are appropriate hints for a confirmed complete supported bcrypt record, not a reason to rewrite a prefix or strip its cost. Inspect the receiving parser/examples if it rejects the record. Format identification is not password recovery; an exhausted candidate set is not a password-strength verdict.

A recovered password verifies a candidate against this selected application record at acquisition time. Testing a selected SSH/application login, if authorized, is separate evidence of reuse/current access. Database user, Joomla user, blocked state, application role and OS effective UID must remain distinct. Finish with endpoint/version/query, selected account/ID and complete format or the specific missing/ambiguous evidence. No SQL writes or application password reset are needed for acquisition.

Use the pinned [Joomla users schema](https://github.com/joomla/joomla-cms/blob/4.2.6/installation/sql/mysql/base.sql), [password helper](https://github.com/joomla/joomla-cms/blob/4.2.6/libraries/src/User/UserHelper.php), [MySQL connection rules](https://dev.mysql.com/doc/refman/8.0/en/connecting.html) and [classic/X protocol distinction](https://dev.mysql.com/doc/refman/8.0/en/connecting-using-dns-srv.html) to resolve mismatches.
