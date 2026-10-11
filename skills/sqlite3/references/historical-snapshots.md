# Compare authentication metadata across retained snapshots

Use coherent, existing working copies with recorded acquisition times and fingerprints. A filename containing a month is a label, not proof of acquisition order. Inspect each snapshot's actual schema; migrations can change table names, identifiers or the encoding of a field. Keep the original archives and their database/WAL context intact.

Use the entrypoint's read-only, startup-free CLI invocation with a reviewed bounded SELECT. The following query uses an **illustrative schema** `accounts(id, username, password)` and a selected account ID of 7. Adapt it only after confirming the columns and identifier:

~~~sql
SELECT id, username, typeof(password) AS storage_type,
       CASE
         WHEN password IS NULL THEN 'null'
         WHEN password = '' THEN 'empty'
         WHEN typeof(password) != 'text' THEN 'non-text'
         WHEN instr(password, '$') > 1
           THEN substr(password, 1, instr(password, '$') - 1)
         ELSE 'unclassified'
       END AS format_prefix
FROM accounts
WHERE id = 7
LIMIT 1;
~~~

For application formats with a documented leading algorithm name, this returns metadata without printing the verifier. A prefix is a classification clue; validate its meaning against the application's writer/parser. Formats beginning with `$`, bare digests, binary fields and malformed text remain unclassified. Missing accounts and changed identity mappings require reconciliation before comparing rows.

An **illustrative** comparison might report `sha1` in an older snapshot and `pbkdf2_sha256` in a later one. This supports a change in that stored account's format. It does not establish the current application's enabled algorithms, a password change, current login validity or every user's migration status. Check the application's migration/rehash policy separately. Stronger current storage does not remove copies retained in older backups; report the affected snapshots and their access/retention context for the owner's remediation decision.

Finish with snapshot identity, selected account mapping, observed format metadata and unresolved acquisition/schema questions. Preserve failed-query status rather than treating empty output as absence.

For function and CLI behavior, consult SQLite's [scalar functions](https://www.sqlite.org/lang_corefunc.html) and [command-line shell](https://www.sqlite.org/cli.html).
